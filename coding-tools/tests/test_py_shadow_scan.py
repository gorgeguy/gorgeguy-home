from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from py_shadow_scan import analyze_file


class ShadowScanInitImportTests(unittest.TestCase):
    def write_file(self, path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_shadows_implicit_submodule_relative_import(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pkg_dir = Path(tmp_dir) / "mypkg"
            self.write_file(pkg_dir / "data.py", "def load_data():\n    return 1\n")
            self.write_file(
                pkg_dir / "__init__.py",
                "from .data import load_data\n\n"
                "def run():\n"
                "    data = load_data()\n"
                "    return data\n",
            )

            issues = analyze_file(pkg_dir / "__init__.py", "lexical")

            self.assertEqual([issue.name for issue in issues], ["data"])
            self.assertEqual(issues[0].kind, "implicit submodule")

    def test_shadows_implicit_submodule_absolute_import(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pkg_dir = Path(tmp_dir) / "mypkg"
            self.write_file(pkg_dir / "data.py", "def load_data():\n    return 1\n")
            self.write_file(
                pkg_dir / "__init__.py",
                "from mypkg.data import load_data\n\n"
                "def run():\n"
                "    data = load_data()\n"
                "    return data\n",
            )

            issues = analyze_file(pkg_dir / "__init__.py", "lexical")

            self.assertEqual([issue.name for issue in issues], ["data"])
            self.assertEqual(issues[0].kind, "implicit submodule")

    def test_no_false_positive_in_regular_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pkg_dir = Path(tmp_dir) / "mypkg"
            self.write_file(pkg_dir / "data.py", "def load_data():\n    return 1\n")
            self.write_file(
                pkg_dir / "runner.py",
                "from mypkg.data import load_data\n\n"
                "def run():\n"
                "    data = load_data()\n"
                "    return data\n",
            )

            issues = analyze_file(pkg_dir / "runner.py", "lexical")

            self.assertEqual(issues, [])

    def test_no_duplicate_with_explicit_dot_import(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pkg_dir = Path(tmp_dir) / "mypkg"
            self.write_file(pkg_dir / "data.py", "def load_data():\n    return 1\n")
            self.write_file(
                pkg_dir / "__init__.py",
                "from . import data\n\n"
                "def run():\n"
                "    data = 1\n"
                "    return data\n",
            )

            issues = analyze_file(pkg_dir / "__init__.py", "lexical")

            self.assertEqual(len(issues), 1)
            self.assertEqual(issues[0].name, "data")

    def test_level_two_relative_not_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            pkg_dir = Path(tmp_dir) / "mypkg" / "nested"
            self.write_file(Path(tmp_dir) / "mypkg" / "sibling.py", "X = 1\n")
            self.write_file(
                pkg_dir / "__init__.py",
                "from ..sibling import X\n\n"
                "def run():\n"
                "    sibling = X\n"
                "    return sibling\n",
            )

            issues = analyze_file(pkg_dir / "__init__.py", "lexical")

            self.assertEqual(issues, [])

    def test_nested_function_shadows_outer_name_declared_later(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "example.py"
            self.write_file(
                path,
                "def outer(work_queue, pending, executor):\n"
                "    queue_idx = 0\n\n"
                "    def submit_batch():\n"
                "        nonlocal queue_idx\n"
                "        key, src_prefix = work_queue[queue_idx]\n"
                "        fut = executor.submit(str, key)\n"
                "        return fut, src_prefix\n\n"
                "    for fut in pending:\n"
                "        key, src_prefix = pending[fut]\n"
                "        return key, src_prefix\n",
            )

            issues = analyze_file(path, "lexical")
            issue_names = {issue.name for issue in issues}

            self.assertEqual(issue_names, {"fut", "key", "src_prefix"})


if __name__ == "__main__":
    unittest.main()
