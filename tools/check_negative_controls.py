"""Run real gates on harmless mutations in temporary copies, never the working tree.

A nonzero exit alone is insufficient: require the expected diagnostic too. The
dependency probe queries public advisory metadata without installing vulnerable code.
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rejects(directory, command, diagnostic):
    result = subprocess.run(
        command,
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
            ".github/workflows/shadow-tests.yml",
            "actions/checkout@11d5960a326750d5838078e36cf38b85af677262",
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
    with tempfile.TemporaryDirectory() as temporary:
        copy = Path(temporary) / "repo"
        copy.mkdir()
        for name in ("project_live", "tests", "tools", "docs", ".github", "data", "requirements"):
            shutil.copytree(ROOT / name, copy / name, ignore=shutil.ignore_patterns("__pycache__"))
        for path in ROOT.glob("*.md"):
            shutil.copy2(path, copy / path.name)
        for name in ("pyproject.toml", "LICENSE", ".gitignore"):
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
