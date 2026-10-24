"""C-01/H-01/S-01/V-01: static edges for the current offline starter (ADR 0001).

This explicit inventory catches new capability imports and reversed dependencies.
It is not Python sandboxing, a call graph, or proof against reflective hostile code.
"""

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_IMPORTS = {
    "__init__": set(),
    "events": {"__future__", "json", "dataclasses", "datetime", "typing"},
    "safety_boundary": {"__future__", "dataclasses"},
    "context": {"__future__", "dataclasses", "math", "datetime", "project_live.events"},
    "environment": {"__future__", "dataclasses", "datetime", "project_live.events"},
    "replay": {
        "__future__",
        "json",
        "pathlib",
        "project_live.events",
        "project_live.context",
        "project_live.environment",
        "project_live.safety_boundary",
    },
    "bayes": {"dataclasses", "datetime", "itertools", "math"},
    "sensing": {"dataclasses", "datetime", "math"},
    "pipeline": {
        "json",
        "datetime",
        "pathlib",
        "project_live.bayes",
        "project_live.sensing",
        "project_live.safety_boundary",
    },
    "history": {
        "json",
        "dataclasses",
        "datetime",
        "pathlib",
        "project_live.bayes",
        "project_live.sensing",
        "project_live.safety_boundary",
    },
    "cli": {
        "argparse",
        "json",
        "project_live.replay",
        "project_live.pipeline",
        "project_live.history",
    },
}


class ArchitectureTests(unittest.TestCase):
    def test_current_module_inventory_and_import_boundaries(self):
        paths = list((ROOT / "project_live").rglob("*.py"))
        self.assertEqual(
            {p.relative_to(ROOT / "project_live").as_posix() for p in paths},
            {f"{module}.py" for module in ALLOWED_IMPORTS},
        )
        for path in paths:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                with self.subTest(file=path.name, line=getattr(node, "lineno", 0)):
                    if isinstance(node, ast.Import):
                        imports = {alias.name for alias in node.names}
                    elif isinstance(node, ast.ImportFrom):
                        self.assertLessEqual(node.level, 1, "outside-package relative import")
                        imports = {f"project_live.{node.module}" if node.level else node.module}
                        self.assertNotIn("*", {alias.name for alias in node.names})
                    else:
                        imports = set()
                    self.assertFalse(
                        imports - ALLOWED_IMPORTS[path.stem], f"unreviewed import edge: {imports}"
                    )
                    if isinstance(node, ast.Name):
                        self.assertNotIn(
                            node.id,
                            {"__import__", "eval", "exec", "compile"},
                            "dynamic execution is outside this starter's contract",
                        )

    def test_runtime_dependency_additions_need_explicit_boundary_review(self):
        import tomllib

        project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
        self.assertFalse(project.get("dependencies"), "update dependency/capability review first")
        self.assertFalse(project.get("optional-dependencies"))
        self.assertFalse(project.get("dynamic"))
