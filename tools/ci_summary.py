"""Render actual step outcomes and gaps; never infer claim support from test totals."""

import argparse
import json
import os
import platform
import re
from pathlib import Path


def check_audit():
    report = json.loads(Path("audit.json").read_text())
    expected = {
        (name.lower().replace("_", "-").replace(".", "-"), version)
        for name, version in re.findall(
            r"^([\w.-]+)==([^\s\\]+)", Path("requirements/ci.txt").read_text(), re.MULTILINE
        )
    }
    checked = set()
    for item in report["dependencies"]:
        if "skip_reason" in item or item.get("vulns"):
            raise ValueError(f"Unverified or vulnerable dependency: {item['name']}")
        checked.add((item["name"].lower().replace("_", "-").replace(".", "-"), item["version"]))
    if not expected or checked != expected:
        raise ValueError("Advisory report does not cover the complete pinned dependency graph")
    print(f"PASS advisory coverage: all {len(checked)} locked packages checked; none skipped")


def main():
    lines = [
        "## Synthetic software verification",
        "",
        f"Revision: `{os.environ.get('GITHUB_SHA', 'local/unrecorded')}`; "
        f"Python {platform.python_version()}",
        "",
        "| Check | Observed step outcome |",
        "| --- | --- |",
    ]
    for name in (
        "install",
        "lint",
        "format",
        "actions",
        "docs",
        "tests",
        "replay",
        "coverage",
        "negative",
        "audit",
        "diff",
    ):
        outcome = os.environ.get(f"RESULT_{name.upper()}", "not run / unavailable")
        lines.append(f"| {name} | {outcome} |")
    lines += [
        "",
        "A skipped, cancelled or missing check is not a pass. "
        "Passing negative controls means the synthetic violation was detected.",
        "",
        "### Measured code coverage (including missing lines/branches)",
        "",
    ]
    coverage = Path("coverage.txt")
    if coverage.exists():
        lines += ["```text", coverage.read_text().strip(), "```"]
    else:
        lines.append("NOT MEASURED: no coverage report was produced.")
    lines += [
        "",
        "Coverage is execution evidence, not assertion quality or hazard coverage. "
        "No percentage establishes safety.",
        "",
        "### Claim status from the reviewed record",
        "",
        "These are recorded limitations, not new CI verdicts or independent approval.",
        "",
        "| Claim | Recorded conclusion |",
        "| --- | --- |",
    ]
    for row in Path("docs/assurance/CLAIMS_MATRIX.md").read_text().splitlines():
        if row.startswith("| **C-"):
            cells = row.split("|")
            conclusion = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cells[5].strip())
            lines.append(f"| {cells[1].split(':')[0].strip()}** | {conclusion} |")
    lines += [
        "",
        "Missing system evidence includes V-03–V-05 and V-07–V-09. "
        "V-01/V-02/V-06 remain partial. No clinical validation, host isolation, "
        "standards compliance, independent review or release approval is established.",
        "",
    ]
    report = "\n".join(lines)
    print(report)
    if summary := os.environ.get("GITHUB_STEP_SUMMARY"):
        with Path(summary).open("a") as output:
            output.write(report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-audit", action="store_true")
    args = parser.parse_args()
    check_audit() if args.check_audit else main()
