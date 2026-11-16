# Public multi-platform Python index resolved 2026-11-16; see image-lock.json.
FROM python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b
WORKDIR /app
COPY requirements-service.txt ./
RUN python -m pip install --no-cache-dir --require-hashes --only-binary=:all: -r requirements-service.txt
COPY src/preemption_api.py src/surfer_session.py src/voi_attention_gate.py ./
USER 65532:65532
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
CMD ["uvicorn", "preemption_api:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--no-access-log"]
