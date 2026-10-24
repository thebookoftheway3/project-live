"""Parse CI/config YAML and the existing GitHub issue-template front matter."""

from pathlib import Path

import yaml


def main():
    paths = sorted(Path(".github").rglob("*.yml")) + sorted(Path(".github").rglob("*.yaml"))
    for path in paths:
        # BaseLoader keeps YAML 1.1's `on` boolean conversion out of workflow parsing.
        value = yaml.load(path.read_text(), Loader=yaml.BaseLoader)
        if not isinstance(value, dict):
            raise ValueError(f"{path}: expected a YAML mapping")
        print(f"PASS YAML {path}")
    for path in sorted(Path(".github/ISSUE_TEMPLATE").glob("*.md")):
        text = path.read_text()
        if not text.startswith("---\n") or len(text.split("---\n", 2)) != 3:
            raise ValueError(f"{path}: missing delimited front matter")
        metadata = yaml.safe_load(text.split("---\n", 2)[1])
        for field in ("name", "about", "title", "labels", "assignees"):
            if not isinstance(metadata.get(field), str):
                raise ValueError(f"{path}: missing/string field {field}")
        print(f"PASS template {path}")


if __name__ == "__main__":
    main()
