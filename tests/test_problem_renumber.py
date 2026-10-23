"""Renumber Dormitory Lights without losing submission history."""
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

import server
import judge


class DormitoryRenumberTests(unittest.TestCase):
    def test_database_migration_preserves_submission_details_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as work:
            path = Path(work) / 'course.db'
            with patch.object(server, 'DB', path):
                server.init_db()
                with sqlite3.connect(path) as db:
                    db.executemany(
                        'insert into submissions(id,user,book,problem,result,source,detail) values (?,?,?,?,?,?,?)',
                        [(1,'student','practice','31419','Accepted','source','detail'),
                         (2,'student','practice','31270','Wrong Answer','new','new-detail'),
                         (3,'student','routine','31419','Accepted','other','other-detail')])
                server.init_db()
                server.init_db()
            with sqlite3.connect(path) as db:
                rows = db.execute('select id,book,problem,result,source,detail from submissions order by id').fetchall()
            self.assertEqual(rows, [(1,'practice','31270','Accepted','source','detail'),
                                    (2,'practice','31270','Wrong Answer','new','new-detail'),
                                    (3,'routine','31419','Accepted','other','other-detail')])

    def test_catalog_uses_corrected_id_and_original_tests(self):
        self.assertIsNone(judge.catalog_item('practice', '31419'))
        row = judge.catalog_item('practice', '31270')
        self.assertEqual(row['global_number'], 31270)
        # 2026-10-23 后台下载（fetch_gmyhf_testdata.py）发现平台原始数据已从 2 组
        # 扩充到 37 组，_GMyhf 已同步为平台当前数据。
        self.assertEqual(row['test_count'], 37)
        self.assertIn('31270:', server.catalog_title(row))
        self.assertIn('宿舍熄灯', server.catalog_title(row))
        for case in row['test_cases']:
            self.assertIn('/31270_GMyhf/', case['input'])
            self.assertTrue((server.MIRROR / case['input']).is_file())
        dates = json.loads((server.MIRROR / 'added_dates.json').read_text())
        self.assertEqual(dates['practice/31270'], '2026-10-15')
        self.assertNotIn('practice/31419', dates)
