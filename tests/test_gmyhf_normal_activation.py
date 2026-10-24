"""六题真实本地绑定：题面、样例、限额和全部自产数据必须指向同一题。"""
import json
from pathlib import Path
import unittest

import judge
import server
from scripts import index_tests
from tests.test_gmyhf_missing_normal_data import NUMBERS, directory

MIRROR=Path(__file__).resolve().parents[1]/'data/openjudge'


class NormalActivationTests(unittest.TestCase):
    def test_real_bindings_pages_limits_and_samples(self):
        handler=object.__new__(server.Handler)
        parser=index_tests.BookStatsParser()
        book=(MIRROR/'books/practice__11.html').read_text()
        parser.feed(book)
        for number in NUMBERS:
            with self.subTest(number=number):
                item=judge.catalog_item('practice',str(number))
                self.assertIsNotNone(item)
                self.assertEqual(number,item['global_number'])
                self.assertTrue(item['tests'])
                self.assertEqual(21,item['test_count'])
                actual={(c['input'],c['output']) for c in item['test_cases']}
                expected={(str(p.relative_to(MIRROR)),str(p.with_suffix('.out').relative_to(MIRROR)))
                          for p in (directory(number)/'data').glob('*.in')}
                self.assertEqual(expected,actual)
                self.assertNotIn('checker',item)
                page=MIRROR/f'pages/practice__{number}.html'
                self.assertEqual(number,index_tests.read_global_number(page))
                title,params,content,_=handler.problem_parts(page,'practice',str(number))
                self.assertIn(item['title'],title)
                self.assertIn('65536kB',params)
                self.assertNotIn('<script',content)
                sample=handler.sample_io(page)
                for key,suffix in [('input','in'),('output','out')]:
                    self.assertEqual((directory(number)/f'data/0.{suffix}').read_text().rstrip('\n'),sample[key])
                self.assertEqual(1,sum(r['id']==str(number) for r in parser.rows))
                self.assertEqual(2,book.count(f'href="/practice/{number}/"'))
                self.assertEqual({'total_ms':1000,'case_ms':100 if number in (31178,31200) else 1000,
                                  'memory_kb':65536},judge.problem_limits(number))

    def test_resource_benchmarks_stay_excluded(self):
        catalog=json.loads((MIRROR/'catalog.json').read_text())
        for item in catalog['problems']:
            if item.get('global_number') in range(31028,31033):
                self.assertFalse(item.get('tests'))
                self.assertFalse(item.get('test_cases'))
