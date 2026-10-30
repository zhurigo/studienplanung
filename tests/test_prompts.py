"""
Tests for the shared input helpers.

Run with:  python -m unittest discover tests
"""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from planner.prompts import ask_number, ask_yes_no, pause


class PromptWordingTests(unittest.TestCase):
    """The retry lines match docs/app_flow.md §5, including the period."""

    def test_ask_number_rejects_text(self):
        with patch("builtins.input", side_effect=["abc", "3"]):
            with redirect_stdout(io.StringIO()) as output:
                answer = ask_number("Pick: ", 1, 3)

        self.assertEqual(answer, 3)
        self.assertIn("Please enter a number from 1 to 3",
                      output.getvalue())

    def test_ask_yes_no_rejects_other_words(self):
        with patch("builtins.input", side_effect=["yes", "n"]):
            with redirect_stdout(io.StringIO()) as output:
                answer = ask_yes_no("Continue? (y/n): ")

        self.assertFalse(answer)
        self.assertIn("Please enter y or n", output.getvalue())

    def test_pause_accepts_any_input_once(self):
        with patch("builtins.input", return_value="xyz") as mocked:
            with redirect_stdout(io.StringIO()):
                result = pause()

        self.assertIsNone(result)
        self.assertEqual(mocked.call_count, 1)
        self.assertIn("Press Enter to return", mocked.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
