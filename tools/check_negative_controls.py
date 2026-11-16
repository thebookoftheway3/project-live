"""Run real gates on harmless mutations in temporary copies, never the working tree.

A nonzero exit alone is insufficient: require the expected diagnostic too. The
dependency probe queries public advisory metadata without installing vulnerable code.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rejects(directory, command, diagnostic):
    # Repeated same-size mutations within one second must not reuse stale bytecode.
    result = subprocess.run(
        command,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        cwd=directory,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
        check=False,
    )
    if result.returncode == 0 or diagnostic not in result.stdout:
        raise AssertionError(f"Gate did not detect {diagnostic!r}: {command}\n{result.stdout}")
    print(f"DETECTED {diagnostic}: exit {result.returncode}; {' '.join(command)}")


def offline_controls():
    # Mutate the reviewed pin, so legitimate Action upgrades keep testing the gate.
    workflow = (ROOT / ".github/workflows/shadow-tests.yml").read_text()
    checkout_pin = re.search(r"\bactions/checkout@[0-9a-f]{40}\b", workflow)
    if checkout_pin is None:
        raise AssertionError("Missing full checkout SHA; run the workflow security gate")
    probes = [
        (
            "project_live/safety_boundary.py",
            "\nunknown_symbol\n",
            ["ruff", "check", "project_live"],
            "F821",
        ),
        (
            "project_live/safety_boundary.py",
            "\nx=  1\n",
            ["ruff", "format", "--check", "project_live"],
            "would be reformatted",
        ),
        (
            "project_live/events.py",
            "\nfrom project_live import replay\n",
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-p",
                "test_architecture.py",
            ],
            "unreviewed import edge",
        ),
        (
            "project_live/context.py",
            "\nimport socket\n",
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-p",
                "test_architecture.py",
            ],
            "unreviewed import edge",
        ),
        (
            "README.md",
            "\n[broken](missing-synthetic-document.md)\n",
            ["rumdl", "check", "."],
            "MD057",
        ),
        ("README.md", "\n[broken](#missing-synthetic-heading)\n", ["rumdl", "check", "."], "MD051"),
    ]
    replacements = [
        (
            "project_live/bayes.py",
            "if leaves.intersection(evidence.source_ids) or groups.intersection(\n"
            "            evidence.dependence_groups\n        ):",
            "if False:",
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-p",
                "test_bayesian_pipeline.py",
            ],
            "test_duplicate_leaf_and_shared_error_group_are_withheld",
        ),
        (
            "project_live/sensing.py",
            "if not policy.permits(completed) or frame.access_reason(completed):",
            "if False:",
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-p",
                "test_bayesian_pipeline.py",
            ],
            "test_midflight_revocation_and_expiry_withhold_results",
        ),
        (
            "project_live/pipeline.py",
            "if cutoff is not None and sample.available_at > cutoff:",
            "if False:",
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-p",
                "test_bayesian_pipeline.py",
            ],
            "test_late_arrival_and_result_cannot_leak_into_earlier_cutoff",
        ),
        (
            ".github/workflows/shadow-tests.yml",
            checkout_pin[0],
            "actions/checkout@v4",
            [
                "zizmor",
                "--offline",
                "--no-progress",
                "--strict-collection",
                "--persona",
                "auditor",
                ".github",
            ],
            "unpinned-uses",
        ),
        (
            ".github/workflows/shadow-tests.yml",
            "contents: read",
            "contents: write",
            [
                "zizmor",
                "--offline",
                "--no-progress",
                "--strict-collection",
                "--persona",
                "auditor",
                ".github",
            ],
            "excessive-permissions",
        ),
        (
            "docs/assurance/CLAIMS_MATRIX.md",
            "E01 tests",
            "E99 tests",
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-p",
                "test_traceability.py",
            ],
            "undefined evidence",
        ),
        (
            "project_live/safety_boundary.py",
            "Authorization(False,",
            "Authorization(True,",
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-p",
                "test_non_actuation.py",
            ],
            "True is not False",
        ),
        (
            "project_live/safety_boundary.py",
            'raise PermissionError("NoPumpAccess: live insulin delivery intentionally unavailable")',
            "return None",
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-p",
                "test_non_actuation.py",
            ],
            "PermissionError not raised",
        ),
    ]
    history_command = [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests",
        "-p",
        "test_history.py",
    ]
    for old, new, diagnostic in (
        (
            "if item.available_at > cutoff:",
            "if False:",
            "test_evidence_availability_duplicates_and_shared_leaves",
        ),
        (
            "if sample.available_at > as_of:",
            "if False:",
            "test_direct_retrieval_filters_asof_before_ranking",
        ),
        (
            "elif not frame.payload_present:",
            "elif False:",
            "test_current_permissions_retention_and_missing_payload_fail_closed",
        ),
        (
            "elif sensor_available > online:",
            "elif False:",
            "test_late_source_and_later_sensor_cannot_leak",
        ),
    ):
        replacements.append(("project_live/history.py", old, new, history_command, diagnostic))
    loop_command = [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests",
        "-p",
        "test_loop_observations.py",
    ]
    for old, new, diagnostic in (
        (
            'if not item.synthetic and (not consent or os.environ.get("GITHUB_ACTIONS") == "true"):',
            "if False:",
            "test_real_data_requires_consent_and_is_refused_in_ci",
        ),
        (
            "(i for i in items if i.received_at <= as_of)",
            "(i for i in items)",
            "test_asof_excludes_late_arrivals_without_rewriting_earlier_snapshots",
        ),
        (
            "if item.display_only or item.user_entered or item.condition is not None:",
            "if False:",
            "test_quality_markers_are_not_treated_as_exact_measurements",
        ),
    ):
        replacements.append(
            ("project_live/loop_observations.py", old, new, loop_command, diagnostic)
        )
    # Exercise the C99 target's independent constraints with diagnostic matching.
    for old, new, diagnostic in (
        (
            "{s, in.scheduled, true, MMU_SCHEDULE}",
            "{s, in.requested, true, MMU_SCHEDULE}",
            "zero upward invariant",
        ),
        (
            "if (!s.green)",
            "if (in.request_green)",
            "renewal cannot extend lease",
        ),
        ("in.now_ms < s.carb_until_ms", "false", "carb guard"),
        ("in.now_ms < s.concert_until_ms", "false", "concert guard"),
        ("in.now_ms < s.lockout_until_ms", "false", "reset lockout"),
        ("sum_o * 100 < sum_s * 55", "sum_o * 100 < sum_s * 54", "historical deficit rejected"),
        ("i < minutes", "i < 1", "whole duration budget"),
    ):
        replacements.append(
            (
                "wp1-deterministic-mmu-bridge/firmware/src/conflict_monitor.c",
                old,
                new,
                ["sh", "tools/check_mmu.sh"],
                diagnostic,
            )
        )
    with tempfile.TemporaryDirectory() as temporary:
        copy = Path(temporary) / "repo"
        copy.mkdir()
        for name in (
            "tests",
            "tools",
            "docs",
            ".github",
            "data",
            "requirements",
            "wp1-deterministic-mmu-bridge",
            "wp2-bayesian-voi-engine",
            "wp3-edge-vision-pipelines",
            "wp4-passive-ui-clients",
        ):
            shutil.copytree(ROOT / name, copy / name, ignore=shutil.ignore_patterns("__pycache__"))
        (copy / "project_live").symlink_to("wp2-bayesian-voi-engine/src/project_live")
        for path in ROOT.glob("*.md"):
            shutil.copy2(path, copy / path.name)
        for name in ("pyproject.toml", "LICENSE", "LICENSE-AGPLv3", ".gitignore"):
            shutil.copy2(ROOT / name, copy / name)
        for name, addition, command, diagnostic in probes:
            path = copy / name
            original = path.read_text()
            try:
                path.write_text(original + addition)
                rejects(copy, command, diagnostic)
            finally:
                path.write_text(original)
        for name, old, new, command, diagnostic in replacements:
            path = copy / name
            original = path.read_text()
            if old not in original:
                raise AssertionError(f"Stale mutation target: {old}")
            try:
                path.write_text(original.replace(old, new, 1))
                rejects(copy, command, diagnostic)
            finally:
                path.write_text(original)


def audit_control():
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory)
        (path / "vulnerable.txt").write_text("django==1.2\n")
        command = [
            sys.executable,
            "-m",
            "pip_audit",
            "--no-deps",
            "--disable-pip",
            "-r",
            "vulnerable.txt",
            "--format",
            "json",
            "-o",
            "audit.json",
        ]
        result = subprocess.run(command, cwd=path, timeout=120, check=False)
        report = json.loads((path / "audit.json").read_text())
        if result.returncode != 1 or not any(
            item["name"] == "django" and item["vulns"] for item in report["dependencies"]
        ):
            raise AssertionError("Advisory negative control failed; no vulnerability detected")
        print("DETECTED known vulnerable django==1.2 metadata; no package installed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()
    audit_control() if args.audit_only else offline_controls()
