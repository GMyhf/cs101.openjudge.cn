"""平台回填的并发变化保护；全部使用自产夹具，不登录真实后台。"""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import repair_gmyhf_pending_answers as repair


class AnswerRepairTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.live = {'a.in': b'3\n', 'a.out': b'6\n', 'notes.txt': b'attachment'}
        self.uploads = []
        self.fields = {'description': 'fixture'}
        self.page = '<textarea name="description">fixture</textarea>' + ''.join(
            f'<a href="/admin/download?problem_id=42&filename={name}">下载</a>'
            for name in self.live)
        source = 'print(7)\n'
        evidence = {'entries': [{'global_number': 42,
                    'authored_reference': {'source': source, 'sha256': repair.sha(source.encode())},
                    'checks': {'statement': {'field_sha256': {'description': repair.sha(b'fixture')}},
                               'readback': {'files': [{'filename': n, 'sha256': repair.sha(v)}
                                                     for n, v in self.live.items() if n != 'notes.txt']},
                               'answers': {'files': [{'input': 'a.in', 'output': 'a.out',
                                           'input_sha256': repair.sha(b'3\n'),
                                           'output_sha256': repair.sha(b'6\n'), 'matches': False}]}}}]}
        repair.save(self.root / 'collab/gmyhf-pending-batch16-review.json', evidence)
        base = self.root / 'data/openjudge/tests/admin_download/42'
        base.mkdir(parents=True)
        for name, value in self.live.items():
            (base / name).write_bytes(value)
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        for target, value in [('ROOT', self.root), ('BATCHES', {1: {42: 16}}), ('COUNTS', {1: 1})]:
            self.stack.enter_context(patch.object(repair, target, value))
        self.stack.enter_context(patch.object(repair.judge, 'judge', return_value={'status': 'Accepted'}))
        self.stack.enter_context(patch.object(repair.subprocess, 'check_output', return_value='fixture-head\n'))
        session = self.stack.enter_context(patch.object(repair.platform.oj_submit, 'Session')).return_value
        session.login.return_value = session
        session._get.side_effect = lambda url: self.page
        self.stack.enter_context(patch.object(repair.platform, 'parse_form', side_effect=lambda page: self.fields))
        self.stack.enter_context(patch.object(repair.platform, 'download', side_effect=lambda s, n, f: self.live[f]))
        self.stack.enter_context(patch.object(repair.platform, 'upload', side_effect=self.upload))
        self.stack.enter_context(contextlib.redirect_stdout(io.StringIO()))

    def upload(self, session, number, name, payload):
        self.uploads.append((number, name))
        self.live[name] = payload

    def run_repair(self, apply=True):
        repair.run(1, self.root / 'work', apply)

    def test_plan_does_not_upload_or_claim_completion(self):
        self.run_repair(False)
        self.assertEqual([], self.uploads)
        self.assertFalse((self.root / 'collab/gmyhf-answer-repairs-batch1.json').exists())

    def test_apply_preserves_input_attachment_and_original_snapshot(self):
        self.run_repair()
        self.assertEqual([(42, 'a.out')], self.uploads)
        self.assertEqual({'a.in': b'3\n', 'a.out': b'7\n', 'notes.txt': b'attachment'}, self.live)
        self.assertEqual(b'6\n', (self.root / 'data/openjudge/tests/admin_download/42/a.out').read_bytes())
        self.assertEqual(b'7\n', (self.root / 'data/openjudge/tests/admin_repaired/42/data/a.out').read_bytes())
        report = json.loads((self.root / 'collab/gmyhf-answer-repairs-batch1.json').read_text())
        self.assertTrue(report['applied'])
        self.assertEqual(repair.sha(b'attachment'), report['problems'][0]['final_files']['notes.txt'])
        self.run_repair()  # 回读与重试幂等，不重复上传。
        self.assertEqual([(42, 'a.out')], self.uploads)

    def test_changed_statement_stops_before_upload(self):
        self.page = self.page.replace('fixture', 'changed')
        with self.assertRaises(ValueError):
            self.run_repair()
        self.assertEqual([], self.uploads)

    def test_changed_input_stops_before_upload(self):
        self.live['a.in'] = b'4\n'
        with self.assertRaises(ValueError):
            self.run_repair()
        self.assertEqual([], self.uploads)

    def test_failed_readback_does_not_claim_completion(self):
        with patch.object(repair.platform, 'upload', return_value=None):
            with self.assertRaises(ValueError):
                self.run_repair()
        self.assertFalse((self.root / 'collab/gmyhf-answer-repairs-batch1.json').exists())

    def test_rejects_download_path_traversal(self):
        with self.assertRaises(ValueError):
            repair.listed_files('<a href="/admin/download?problem_id=42&filename=../x">x</a>', 42)


if __name__ == '__main__':
    unittest.main()
