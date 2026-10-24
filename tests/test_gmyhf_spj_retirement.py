"""课程只撤下31381；平台不支持SPJ的题不能因未来有映射而误接入。"""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import materialize_gmyhf_downloads as materializer
from scripts import retire_gmyhf_31381 as retirement


def course_page(mapping):
    rows = ['<script>var template = \'<form action="/api/contest/modify-problems/">\';</script>']
    for number, global_number in mapping.items():
        rows.append('<form action="/api/contest/modify-problems/">' + ''.join(
            f'<input name="{k}" value="{v}">' for k, v in {
                'contestId': '25952', 'originalNumber': number,
                'problemNumber': number, 'problemId': global_number}.items()) + '</form>')
    return ''.join(rows)


class FakeSession:
    def __init__(self, mapping=None, disturb=False):
        self.mapping = dict(mapping if mapping is not None else {'30686': '30686', 'E31381': '31381', 'test': '31181'})
        self.posts = []
        self.disturb = disturb

    def _get(self, url):
        if url.endswith(retirement.EDIT_PATH):
            return course_page(self.mapping)
        if '/admin/problems/edit/?id=' in url:
            number = url.rsplit('=', 1)[1]
            return (f'<form action="/api/global-problem/modify/"><input name="problemId" value="{number}">'
                    '<input type="radio" name="privacy" value="private" checked></form>'
                    f'<a href="/admin/download?problem_id={number}&amp;filename=0.in">in</a>'
                    f'<a href="/admin/download?problem_id={number}&amp;filename=0.out">out</a>')
        if url.endswith('/2026fallcs101testing/'):
            return ''.join(f'<a href="/2026fallcs101testing/{n}/">题</a>' for n in self.mapping)
        raise AssertionError(url)

    def _post(self, url, fields):
        if not url.endswith('/api/contest/delete-problem/') or fields != {'contestId': '25952', 'problemNumber': 'E31381'}:
            raise AssertionError((url, fields))
        self.posts.append((url, fields))
        del self.mapping['E31381']
        if self.disturb:
            self.mapping['test'] = '99999'
        return '{"result": "SUCCESS"}'


class SpjRetirementTests(unittest.TestCase):
    def run_fake(self, session, apply):
        with tempfile.TemporaryDirectory() as work, \
                patch.object(retirement.common.platform, 'download', return_value=b'original\n'):
            return retirement.run(Path(work), apply=apply, session=session)

    def test_dry_run_apply_and_idempotence(self):
        session = FakeSession()
        plan = self.run_fake(session, False)
        self.assertFalse(plan['applied'])
        self.assertEqual([], session.posts)
        report = self.run_fake(session, True)
        self.assertTrue(report['applied'])
        self.assertEqual(['E31381'], report['removed_routes'])
        self.assertEqual({'30686': '30686', 'test': '31181'}, report['after_mapping'])
        self.assertEqual(1, len(session.posts))
        self.assertTrue(report['test_files_unchanged'])
        self.assertTrue(report['global_forms_unchanged'])
        repeated = self.run_fake(session, True)
        self.assertEqual([], repeated['removed_routes'])
        self.assertEqual(1, len(session.posts))

    def test_ambiguous_binding_stops_before_write(self):
        for mapping in ({'E31381': '12345'}, {'E31381': '31381', 'alias': '31381'}):
            with self.subTest(mapping=mapping):
                session = FakeSession(mapping)
                with self.assertRaises(ValueError):
                    self.run_fake(session, True)
                self.assertEqual([], session.posts)
        for page in ('<p>登录</p>', course_page({'E31381': '31381'}) * 2,
                     course_page({'E31381': '31381'}).replace('25952', '12345')):
            with self.assertRaises(ValueError):
                retirement.course_mapping(page)

    def test_unrelated_mapping_change_is_rejected(self):
        with self.assertRaisesRegex(ValueError, '回读不一致'):
            self.run_fake(FakeSession(disturb=True), True)

    def test_future_catalog_cannot_activate_unbound_spj_downloads(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            downloads = root / 'tests/admin_download'
            downloads.mkdir(parents=True)
            (root / 'collab').mkdir()
            (root / 'collab/valid-contracts.json').write_text('{"dirs": []}')
            manifest = {'fetched_at': 'fixture', 'problems': {}}
            sentinels = []
            for number in (27952, 28341):
                directory = downloads / str(number)
                directory.mkdir()
                files = []
                for name, payload in (('0.in', b'1\n'), ('0.out', b'0\n')):
                    (directory / name).write_bytes(payload)
                    files.append({'filename': name, 'bytes': len(payload),
                                  'sha256': hashlib.sha256(payload).hexdigest()})
                manifest['problems'][str(number)] = {'title': '需要SPJ的题', 'files': files}
                sentinel = root / f'tests/{materializer.bucket_of(number)}/{number}_GMyhf/保留原件'
                sentinel.parent.mkdir(parents=True)
                sentinel.write_bytes(b'original')
                sentinels.append(sentinel)
            (downloads / 'manifest.json').write_text(json.dumps(manifest))
            report = root / 'collab/report.json'
            with patch.multiple(materializer, ROOT=root, TESTS=root / 'tests', DL=downloads, REPORT=report), \
                    patch.object(materializer, 'local_id_map', return_value={27952: '27952', 28341: '28341'}), \
                    patch.object(materializer, 'load_repairs', return_value={}), \
                    patch.object(materializer, 'multi_answer_hit', return_value=None), \
                    patch.object(materializer, 'repair_pair', side_effect=AssertionError('不得接入')) as repair, \
                    contextlib.redirect_stdout(io.StringIO()):
                materializer.main()
                repair.assert_not_called()
            result = json.loads(report.read_text())
            self.assertEqual([], result['materialized'])
            self.assertEqual({27952, 28341}, {r['global_number'] for r in result['skipped']['manual_exclusion']})
            self.assertTrue(all(p.read_bytes() == b'original' for p in sentinels))


if __name__ == '__main__':
    unittest.main()
