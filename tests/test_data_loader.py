"""
Tests for reading the curriculum files.

Alternate flow 11 (docs/app_flow.md §6): a missing or broken file stops
with the §5 message and no traceback.

Run with:  python -m unittest discover tests
"""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from planner.data_loader import DataError, load_electives, load_modules


class DataLoaderErrorTests(unittest.TestCase):
    """Both failure kinds use the same §5 wording."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.data_dir = Path(self.folder.name)

    def write(self, filename, text):
        (self.data_dir / filename).write_text(text, encoding="utf-8")

    def test_invalid_json_raises_data_error(self):
        self.write("electives.json", "{bad")

        with patch("planner.data_loader.DATA_DIR", self.data_dir):
            with self.assertRaises(DataError) as caught:
                load_electives()

        self.assertEqual(
            str(caught.exception),
            "Could not read data/electives.json — stopping",
        )

    def test_wrong_shape_raises_data_error(self):
        self.write("modules.json", "{}")

        with patch("planner.data_loader.DATA_DIR", self.data_dir):
            with self.assertRaises(DataError) as caught:
                load_modules()

        self.assertEqual(
            str(caught.exception),
            "Could not read data/modules.json — stopping",
        )


if __name__ == "__main__":
    unittest.main()
