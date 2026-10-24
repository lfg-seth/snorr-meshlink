"""Regression checks for missing evidence links and failed check propagation."""

import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "check-project.py"
SPEC = importlib.util.spec_from_file_location("check_project", SCRIPT)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class DocumentationLinks(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.page = self.root / "page.md"

    def errors(self, content):
        self.page.write_text(content, encoding="utf-8")
        return checker.link_errors(self.page)

    def test_missing_file_and_heading_fail_with_line_numbers(self):
        errors = self.errors("# Heading\n[missing](absent.md)\n[wrong](#absent)\n")
        self.assertEqual(len(errors), 2)
        self.assertIn(":2: missing file", errors[0])
        self.assertIn(":3: missing heading", errors[1])

    def test_relative_files_spaces_and_duplicate_heading_ids(self):
        (self.root / "evidence file.md").write_text("# Result\n# Result\n", encoding="utf-8")
        errors = self.errors("[ok](<evidence file.md#result-1>)\n[ok](evidence%20file.md#result)\n")
        self.assertEqual(errors, [])

    def test_code_examples_and_external_links_are_not_local_files(self):
        self.assertEqual(self.errors("```md\n[example](missing.md)\n```\n"
                                     "`[inline](missing.md)`\n[external](https://example.invalid/a#b)\n"), [])

    def test_unicode_and_inline_code_heading(self):
        self.assertEqual(self.errors("# 1. Saved `interval` — état\n[ok](#1-saved-interval--état)\n"), [])

    def test_staged_unstaged_and_untracked_docs_are_collected(self):
        calls = iter(["a" * 40, "staged.md\0unstaged.md\0code.py\0", "new.md\0asset.png\0"])
        with patch.object(checker, "ROOT", self.root), patch.object(checker, "git", side_effect=lambda *args: next(calls)):
            self.assertEqual(checker.changed_markdown("HEAD"),
                             [self.root / name for name in ["new.md", "staged.md", "unstaged.md"]])


class CheckFailures(unittest.TestCase):
    def test_failed_suite_returns_nonzero_and_stops_later_scopes(self):
        with patch.object(checker.subprocess, "run", side_effect=subprocess.CalledProcessError(7, ["suite"])), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(checker.main(["bench", "backend"]), 1)
            self.assertEqual(checker.subprocess.run.call_count, 1)

    def test_documentation_failure_propagates(self):
        with patch.object(checker, "check_docs", return_value=1), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(checker.main([]), 1)

    def test_list_never_runs_checks(self):
        with patch.object(checker.subprocess, "run") as run, patch.object(checker, "check_docs") as docs, \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(checker.main(["--list"]), 0)
            run.assert_not_called()
            docs.assert_not_called()


if __name__ == "__main__":
    unittest.main()
