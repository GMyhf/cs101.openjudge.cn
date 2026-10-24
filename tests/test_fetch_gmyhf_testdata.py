"""续传必须核对远端正文；文件长度相同不能证明测试数据未变。"""
import hashlib
import io
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import fetch_gmyhf_testdata as fetch


class FetchDataTests(unittest.TestCase):
    def download(self, folder, payload, force=False, length=None):
        # 旧实现会走仅检查Content-Length的分支；夹具提供该响应以复现漏更新。
        response = io.BytesIO(payload)
        response.headers = {'Content-Length': str(len(payload)) if length is None else length}
        session = SimpleNamespace(_request=lambda url: url,
                                  _opener=SimpleNamespace(open=Mock(return_value=response)))
        with patch.object(fetch, 'session', return_value=session), \
                patch.object(fetch, 'get_bytes', return_value=payload) as download, \
                patch.object(fetch.time, 'sleep'):
            result = fetch.download_one(19964, folder, '1.out', force)
            download.assert_called_once()
            self.assertIn('problem_id=19964&filename=1.out', download.call_args.args[0])
        self.assertEqual(len(payload), result['bytes'])
        self.assertEqual(hashlib.sha256(payload).hexdigest(), result['sha256'])
        self.assertEqual('1.out', result['filename'])
        return result

    def test_equal_size_changed_body_replaces_cached_answer(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            target = folder / '1.out'
            target.write_bytes(b'1\n')
            result = self.download(folder, b'2\n')
            self.assertEqual(b'2\n', target.read_bytes())
            self.assertFalse(result.get('skipped', False))

    def test_equal_body_is_read_back_without_rewriting_cached_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            target = folder / '1.out'
            target.write_bytes(b'42\n')
            os.utime(target, ns=(10**9, 10**9))
            before = target.stat().st_mtime_ns
            result = self.download(folder, b'42\n', length='不是数字')
            self.assertTrue(result['skipped'])
            self.assertEqual(before, target.stat().st_mtime_ns)
            self.assertEqual(b'42\n', target.read_bytes())

    def test_missing_different_length_and_forced_download(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            target = folder / '1.out'
            for old, payload, force in ((None, b'0\n', False),
                                        (b'old', b'12345\n', False),
                                        (b'12345\n', b'12345\n', True)):
                if old is not None:
                    target.write_bytes(old)
                if target.exists():
                    os.utime(target, ns=(10**9, 10**9))
                result = self.download(folder, payload, force)
                self.assertEqual(payload, target.read_bytes())
                self.assertFalse(result.get('skipped', False))
                self.assertNotEqual(10**9, target.stat().st_mtime_ns)

    def test_failed_readback_keeps_old_bytes_and_does_not_report_success(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            target = folder / '1.out'
            target.write_bytes(b'1\n')
            response = io.BytesIO(b'2\n')
            response.headers = {'Content-Length': '2'}
            session = SimpleNamespace(_request=lambda url: url,
                                      _opener=SimpleNamespace(open=Mock(return_value=response)))
            with patch.object(fetch, 'session', return_value=session), \
                    patch.object(fetch, 'get_bytes', side_effect=OSError('回读失败')), \
                    patch.object(fetch.time, 'sleep'), self.assertRaises(OSError):
                fetch.download_one(19964, folder, '1.out', False)
            self.assertEqual(b'1\n', target.read_bytes())


if __name__ == '__main__':
    unittest.main()
