"""废弃题即使未来有题库映射及下载数据，也不能重新物化。"""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import materialize_gmyhf_downloads as materializer

ROOT = Path(__file__).resolve().parents[1]


class DeprecatedExclusionTests(unittest.TestCase):
    def test_future_mapping_cannot_reactivate_deprecated_problems(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            downloads = root / 'tests/admin_download'
            downloads.mkdir(parents=True)
            (root / 'collab').mkdir()
            (root / 'collab/valid-contracts.json').write_text('{"dirs": []}')
            manifest = {'fetched_at': 'fixture', 'problems': {}}
            sentinels = []
            for number in (19945, 20139):
                directory = downloads / str(number)
                directory.mkdir()
                files = []
                for name, payload in (('0.in', b'1\n'), ('0.out', b'0\n')):
                    (directory / name).write_bytes(payload)
                    files.append({'filename': name, 'bytes': len(payload),
                                  'sha256': hashlib.sha256(payload).hexdigest()})
                manifest['problems'][str(number)] = {'title': '废弃题', 'files': files}
                bucket = materializer.bucket_of(number)
                sentinel = root / f'tests/{bucket}/{number}_GMyhf/保留原件'
                sentinel.parent.mkdir(parents=True)
                sentinel.write_bytes(b'original')
                sentinels.append(sentinel)
            (downloads / 'manifest.json').write_text(json.dumps(manifest))
            report_path = root / 'collab/report.json'
            with patch.multiple(materializer, ROOT=root, TESTS=root / 'tests',
                                DL=downloads, REPORT=report_path), \
                    patch.object(materializer, 'local_id_map', return_value={19945: '19945', 20139: '20139'}), \
                    patch.object(materializer, 'load_repairs', return_value={}), \
                    patch.object(materializer, 'multi_answer_hit', return_value=None), \
                    patch.object(materializer, 'repair_pair', side_effect=AssertionError('废弃题不应进入处理')) as repair, \
                    contextlib.redirect_stdout(io.StringIO()):
                materializer.main()
                repair.assert_not_called()
            report = json.loads(report_path.read_text())
            self.assertEqual([], report['materialized'])
            self.assertEqual({19945, 20139}, {row['global_number']
                                             for row in report['skipped']['manual_exclusion']})
            self.assertTrue(all(path.read_bytes() == b'original' for path in sentinels))

    def test_actual_catalog_keeps_both_deprecated_problems_inactive(self):
        catalog = json.loads((ROOT / 'data/openjudge/catalog.json').read_text())
        active = {int(row['global_number']) for row in catalog['problems']
                  if row.get('global_number') and row.get('test_cases')}
        self.assertTrue({19945, 20139}.isdisjoint(active))


if __name__ == '__main__':
    unittest.main()
