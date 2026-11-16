# SPDX-License-Identifier: AGPL-3.0-only
"""Authenticated, synthetic session API. No therapy override or outgoing voice call."""

import os
import secrets
import time
from dataclasses import asdict
from math import isfinite
from threading import Lock
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field, field_validator
from surfer_session import SemanticEvent, SurferSession


class SyntheticBody(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    synthetic: Literal[True]

    @field_validator("synthetic", mode="before")
    @classmethod
    def exact_synthetic(cls, value):
        if value is not True:
            raise ValueError("explicit synthetic=true required")
        return value


class Clearance(SyntheticBody):
    request_id: str = Field(min_length=1, max_length=64, pattern=r"^[a-zA-Z0-9_-]+$")
    clearance_minutes: int = Field(ge=1, le=180)
    synthetic: Literal[True]


class VoiceCallback(SyntheticBody):
    model_config = ConfigDict(extra="forbid", strict=True)
    request_id: str = Field(min_length=1, max_length=64, pattern=r"^[a-zA-Z0-9_-]+$")
    answer: Literal["yes", "no", "unanswered"]
    escalation_level: int = Field(ge=0, le=2)
    synthetic: Literal[True]


class ContextEvent(SyntheticBody):
    model_config = ConfigDict(extra="forbid", strict=True)
    event_id: str = Field(min_length=1, max_length=64, pattern=r"^[a-zA-Z0-9_-]+$")
    evidence_id: str = Field(min_length=1, max_length=64, pattern=r"^[a-zA-Z0-9_-]+$")
    source: Literal["home_poe", "home_matstation_2d", "brilliant_halo", "brilliant_frame"]
    action: Literal["meal_candidate", "chewing_candidate", "kitchen_activity"]
    subject: Literal["self", "bystander", "unknown"]
    observed_at: float = Field(ge=0, allow_inf_nan=False)
    available_at: float = Field(ge=0, allow_inf_nan=False)
    synthetic: Literal[True]
    consent: bool
    evsi: float = Field(ge=0, allow_inf_nan=False)
    attention_cost: float = Field(ge=0, allow_inf_nan=False)


class OneBitReply(SyntheticBody):
    model_config = ConfigDict(extra="forbid", strict=True)
    question_id: str = Field(min_length=1, max_length=64)
    answer: bool | None
    synthetic: Literal[True]


def create_app(*, token: str | None = None, clock=time.monotonic) -> FastAPI:
    configured = token if token is not None else os.environ.get("LIVE_RESEARCH_API_TOKEN", "")
    if type(configured) is not str or len(configured) < 32 or not configured.isascii():
        raise ValueError("a local ASCII bearer token of at least 32 characters is required")
    app = FastAPI(title="Surfer OS / Project LIVE research API", docs_url=None, redoc_url=None)
    bearer = HTTPBearer(auto_error=False)
    lock = Lock()
    events = {}
    state = {"until": 0.0, "last_clock": clock()}
    if not isfinite(state["last_clock"]) or state["last_clock"] < 0:
        raise ValueError("finite nonnegative clock required")
    origin = state["last_clock"]
    session = SurferSession()

    def authenticate(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
        if credentials is None or not secrets.compare_digest(
            credentials.credentials.encode(), configured.encode()
        ):
            raise HTTPException(401, "authentication required")

    def now():
        tick = clock()
        if not isfinite(tick) or tick < state["last_clock"]:
            raise HTTPException(503, "session clock regressed")
        state["last_clock"] = tick
        return tick

    @app.get("/health")
    def health():
        return {"product": "Surfer OS", "mode": "synthetic", "may_actuate_insulin": False}

    @app.get("/v1/status", dependencies=[Depends(authenticate)])
    def status():
        with lock:
            remaining = max(0, state["until"] - now())
            return {"clearance_seconds_remaining": remaining, "may_actuate_insulin": False}

    @app.post("/v1/preemptions", dependencies=[Depends(authenticate)])
    def preempt(body: Clearance):
        with lock:
            tick = now()
            key = ("clearance", body.request_id)
            payload = body.model_dump()
            if key in events:
                if events[key][0] != payload:
                    raise HTTPException(409, "request ID conflict")
                return events[key][1]
            if len(events) >= 1000:
                raise HTTPException(429, "synthetic session capacity exhausted")
            # Do not allow new request IDs to renew an active clearance indefinitely.
            if tick < state["until"]:
                raise HTTPException(409, "clearance already active")
            session.preempt(now=tick - origin, clearance_minutes=body.clearance_minutes)
            state["until"] = tick + body.clearance_minutes * 60
            result = {"accepted": True, "scope": "synthetic_session", "may_actuate_insulin": False}
            events[key] = (payload, result)
            return result

    @app.post("/v1/events/context", dependencies=[Depends(authenticate)])
    def context(body: ContextEvent):
        with lock:
            tick = now() - origin
            try:
                event = SemanticEvent(
                    **body.model_dump(exclude={"consent", "evsi", "attention_cost"})
                )
                reason, prompt = session.consider(
                    event,
                    now=tick,
                    evsi=body.evsi,
                    base_cost=body.attention_cost,
                    consent=body.consent,
                )
            except ValueError as error:
                raise HTTPException(422, str(error)) from None
            return {
                "status": reason,
                "prompt": asdict(prompt) if prompt else None,
                "may_actuate_insulin": False,
            }

    @app.post("/v1/feedback/1bit", dependencies=[Depends(authenticate)])
    def feedback(body: OneBitReply):
        with lock:
            try:
                result = session.reply(
                    now=now() - origin, question_id=body.question_id, answer=body.answer
                )
            except ValueError as error:
                raise HTTPException(409, str(error)) from None
            return {"status": result, "may_actuate_insulin": False}

    @app.post("/v1/voice/callbacks", dependencies=[Depends(authenticate)])
    def callback(body: VoiceCallback):
        with lock:
            now()
            key = ("voice", body.request_id)
            payload = body.model_dump()
            if key in events:
                if events[key][0] != payload:
                    raise HTTPException(409, "request ID conflict")
                return events[key][1]
            if len(events) >= 1000:
                raise HTTPException(429, "synthetic session capacity exhausted")
            result = {
                "accepted": True,
                "answer": body.answer,
                "next_escalation_level": min(2, body.escalation_level + 1)
                if body.answer == "unanswered"
                else None,
                "callback_dispatched": False,
                "may_actuate_insulin": False,
            }
            events[key] = (payload, result)
            return result

    return app
