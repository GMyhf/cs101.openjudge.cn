import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import crawl_openjudge


class TargetedRefreshTests(unittest.TestCase):
    def test_refresh_preserves_existing_fields_and_adds_new_problem(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            (data / "pages").mkdir()
            catalog = {
                "source": crawl_openjudge.BASE,
                "updated": "2026-07-29",
                "count": 1,
                "problems": [{
                    "book": "routine",
                    "id": "27150",
                    "path": "/routine/27150/",
                    "tests": True,
                    "test_count": 21,
                }],
            }
            (data / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")

            pages = {
                "/routine/27150/": "<html>corrected routine</html>",
                "/practice/27150/": "<html>new practice</html>",
            }
            with patch.object(crawl_openjudge, "DATA", data), \
                    patch.object(crawl_openjudge, "fetch", side_effect=pages.__getitem__), \
                    patch.object(crawl_openjudge, "mirror_all") as mirror_all:
                crawl_openjudge.refresh_problems(["routine/27150", "practice/27150"])

            refreshed = json.loads((data / "catalog.json").read_text(encoding="utf-8"))
            self.assertEqual(refreshed["count"], 2)
            self.assertEqual(refreshed["problems"][0]["test_count"], 21)
            self.assertEqual(refreshed["problems"][1], {
                "book": "practice",
                "id": "27150",
                "path": "/practice/27150/",
                "tests": False,
            })
            self.assertEqual((data / "pages" / "routine__27150.html").read_text(), "<html>corrected routine</html>")
            self.assertEqual((data / "pages" / "practice__27150.html").read_text(), "<html>new practice</html>")
            mirror_all.assert_called_once_with()

    def test_rejects_invalid_problem_spec(self):
        with self.assertRaisesRegex(ValueError, "expected BOOK/ID"):
            crawl_openjudge.parse_problem_spec("unknown/27150")


if __name__ == "__main__":
    unittest.main()
