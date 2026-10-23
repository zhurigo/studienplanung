"""
Tests for the program entry point.

Alternate flow 15 (docs/app_flow.md §6): Ctrl-C / Ctrl-D ends with
"Goodbye." and exit code 0, without a traceback.

Run with:  python -m unittest discover tests
"""

import subprocess
import sys
import unittest
from pathlib import Path


class EntryPointTests(unittest.TestCase):
    """The process exits cleanly when stdin ends early."""

    def test_empty_stdin_exits_cleanly(self):
        root = Path(__file__).resolve().parent.parent

        result = subprocess.run(
            [sys.executable, "main.py"],
            input="",
            capture_output=True,
            text=True,
            cwd=root,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Goodbye.", result.stdout)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
