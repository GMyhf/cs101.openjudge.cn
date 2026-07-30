import json
import sys
import unittest
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import mirror_openjudge_images as mirror
import server


class ImageMirrorTests(unittest.TestCase):
    def test_manifest_covers_every_remote_image_and_every_file_is_intact(self):
        payload = json.loads(mirror.MANIFEST.read_text(encoding="utf-8"))
        references = mirror.collect_remote_images()
        self.assertEqual(payload["remote_urls"], 200)
        self.assertEqual(set(payload["assets"]), set(references))
        self.assertEqual(mirror.check_manifest(), [])

    def test_every_downloaded_page_renders_without_remote_images(self):
        remaining = []
        for path in mirror.html_files():
            parser = mirror.ImageSources()
            parser.feed(server.Handler.local_page(None, path))
            remote = [source for source in parser.sources
                      if urlparse(source).scheme.lower() in {"http", "https"}]
            if remote:
                remaining.append(f"{path.relative_to(ROOT)}: {remote}")
        self.assertEqual(remaining, [])


if __name__ == "__main__":
    unittest.main()
