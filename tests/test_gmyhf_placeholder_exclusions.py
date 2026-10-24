"""占位和明确待移除题，即使未来补数据及映射也不能自动接入。"""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import materialize_gmyhf_downloads as materializer


class PlaceholderExclusionTests(unittest.TestCase):
    def test_future_downloads_and_mapping_cannot_reactivate_retired_problems(self):
        numbers = (28979, 31195, 31248)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            downloads = root / 'tests/admin_download'
            downloads.mkdir(parents=True)
            (root / 'collab').mkdir()
            (root / 'collab/valid-contracts.json').write_text('{"dirs": []}')
            manifest = {'fetched_at': 'fixture', 'problems': {}}
            sentinels = []
            for number in numbers:
                directory = downloads / str(number)
                directory.mkdir()
                files = []
                for name, payload in (('0.in', b'1\n'), ('0.out', b'0\n')):
                    (directory / name).write_bytes(payload)
                    files.append({'filename': name, 'bytes': len(payload),
                                  'sha256': hashlib.sha256(payload).hexdigest()})
                manifest['problems'][str(number)] = {'title': '未来已补数据和映射', 'files': files}
                sentinel = root / f'tests/{materializer.bucket_of(number)}/{number}_GMyhf/保留原件'
                sentinel.parent.mkdir(parents=True)
                sentinel.write_bytes(b'original')
                sentinels.append(sentinel)
            (downloads / 'manifest.json').write_text(json.dumps(manifest))
            report_path = root / 'collab/report.json'
            with patch.multiple(materializer, ROOT=root, TESTS=root / 'tests', DL=downloads, REPORT=report_path), \
                    patch.object(materializer, 'local_id_map', return_value={n: str(n) for n in numbers}), \
                    patch.object(materializer, 'load_repairs', return_value={}), \
                    patch.object(materializer, 'multi_answer_hit', return_value=None), \
                    patch.object(materializer, 'repair_pair', side_effect=AssertionError('不得重新接入')) as repair, \
                    contextlib.redirect_stdout(io.StringIO()):
                materializer.main()
                repair.assert_not_called()
            report = json.loads(report_path.read_text())
            self.assertEqual([], report['materialized'])
            self.assertEqual(set(numbers), {row['global_number'] for row in report['skipped']['manual_exclusion']})
            self.assertTrue(all(path.read_bytes() == b'original' for path in sentinels))


if __name__ == '__main__':
    unittest.main()
