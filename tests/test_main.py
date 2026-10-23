"""
Tests for the program entry point.

Alternate flow 15 (docs/app_flow.md §6): Ctrl-C / Ctrl-D ends with
"Goodbye." and exit code 0, without a traceback.

Run with:  python -m unittest discover tests
"""

import io
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main
from planner.data_loader import DataError


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

    def test_data_error_exits_with_code_1(self):
        error = DataError(
            "Could not read data/electives.json — stopping."
        )

        with patch("main.load_all", side_effect=error):
            with redirect_stdout(io.StringIO()) as output:
                with self.assertRaises(SystemExit) as caught:
                    main.main()

        self.assertEqual(caught.exception.code, 1)
        self.assertIn(
            "Could not read data/electives.json — stopping.",
            output.getvalue(),
        )


if __name__ == "__main__":
    unittest.main()
