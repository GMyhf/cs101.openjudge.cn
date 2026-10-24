"""三题正式绑定；另三题按用户裁定为占位，不再公开或参与判题。"""
import json
from pathlib import Path
import unittest

import judge
import server
from scripts import index_tests
from tests.test_gmyhf_missing_normal_data import directory

NUMBERS=(27207,29337,29893)

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
                self.assertEqual(f'http://cs101.openjudge.cn/practice/{number}/',item['source_url'])
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


class PlaceholderRetirementTests(unittest.TestCase):
    def test_placeholders_have_no_public_entry_page_or_book_link(self):
        from scripts import crawl_openjudge
        from unittest.mock import patch
        catalog=json.loads((MIRROR/'catalog.json').read_text())
        book=(MIRROR/'books/practice__11.html').read_text()
        for number in (29894,31178,31200):
            self.assertIn(number,index_tests.PLACEHOLDER_EXCLUSIONS)
            self.assertFalse(any(r.get('global_number')==number for r in catalog['problems']))
            self.assertIsNone(judge.catalog_item('practice',str(number)))
            self.assertFalse((MIRROR/f'pages/practice__{number}.html').exists())
            self.assertNotIn(f'/practice/{number}/',book)
            self.assertIn(('practice',str(number)),crawl_openjudge.EXCLUDED_ENTRIES)
            with patch.object(crawl_openjudge,'fetch',side_effect=AssertionError('占位题不得回抓')):
                with self.assertRaisesRegex(ValueError,'excluded problem'):
                    crawl_openjudge.refresh_problems([f'practice/{number}'])

    def test_reindex_excludes_every_corpus_and_alias_even_with_checker(self):
        import contextlib
        import io
        import tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as temporary:
            mirror=Path(temporary);items=[]
            (mirror/'pages').mkdir()
            for number in (29893,29894,31178,31200):
                for book in ('practice','dsapre'):
                    items.append({'book':book,'id':str(number)})
                    (mirror/f'pages/{book}__{number}.html').write_text(
                        f'<dl><dt>全局题号</dt><dd>{number}</dd></dl>')
                bucket='20000-29982' if number<30000 else '30000-'
                for suffix in ('','_made','_GMyhf'):
                    base=mirror/'tests'/bucket/(str(number)+suffix)
                    data=base/'data';data.mkdir(parents=True)
                    (data/'0.in').write_text('1\n');(data/'0.out').write_text('1\n')
                    if number!=29893:(base/'checker.py').write_text('# 有checker也不能重新启用占位题\n')
            (mirror/'catalog.json').write_text(json.dumps({'problems':items}))
            with patch.multiple(index_tests,MIRROR=mirror,TESTS=mirror/'tests'),contextlib.redirect_stdout(io.StringIO()):
                index_tests.main()
            output=json.loads((mirror/'catalog.json').read_text())
            for row in output['problems']:
                self.assertEqual(row['global_number']==29893,row['tests'])
                self.assertEqual(1 if row['global_number']==29893 else 0,row['test_count'])
                if row['global_number']!=29893:
                    self.assertEqual([],row['test_cases'])
                    self.assertNotIn('checker',row)
