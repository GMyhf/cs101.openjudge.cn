"""31381本地启用：真实索引、公开样例、可复现数据及正确/错误程序。"""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import judge
import server
from scripts import index_tests
from tests.test_input_constraints import check_31381

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT/'data/openjudge'
DATA = MIRROR/'tests/30000-/31381_made'


def module_at(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Activation31381Tests(unittest.TestCase):
    def test_catalog_page_samples_and_checker_binding(self):
        item = judge.catalog_item('practice', '31381')
        self.assertEqual(31381, item['global_number'])
        self.assertTrue(item['tests'])
        self.assertEqual(21, item['test_count'])
        self.assertEqual(21, len(item['test_cases']))
        self.assertEqual('tests/30000-/31381_made/checker.py', item['checker'])
        self.assertEqual(item['checker'], index_tests.judge_hooks(item['test_cases'])['checker'])
        self.assertIn(31381, index_tests.SPECIAL_JUDGE_GLOBAL_NUMBERS)
        self.assertIn(31381, index_tests.exclude_special_judge_cases({31381:item['test_cases']}))
        with patch.object(index_tests, 'judge_hooks', return_value={}):
            self.assertNotIn(31381, index_tests.exclude_special_judge_cases({31381:item['test_cases']}))
        page = MIRROR/'pages/practice__31381.html'
        self.assertEqual(31381, index_tests.read_global_number(page))
        handler = object.__new__(server.Handler)
        title, params, content, _ = handler.problem_parts(page, 'practice', '31381')
        self.assertIn('Special Judge 测试', title)
        self.assertIn('1000ms', params)
        self.assertIn('以任何顺序排列', content)
        self.assertNotIn('os.fork', content)
        sample = handler.sample_io(page)
        self.assertEqual((DATA/'data/0.in').read_text().rstrip('\n'), sample['input'])
        self.assertEqual((DATA/'data/0.out').read_text().rstrip('\n'), sample['output'])
        parser = index_tests.BookStatsParser()
        parser.feed((MIRROR/'books/practice__11.html').read_text())
        self.assertEqual(1, sum(row['id']=='31381' for row in parser.rows))
        self.assertEqual({'total_ms':1000, 'case_ms':None, 'memory_kb':65536}, judge.problem_limits(31381))

    def test_generator_reproduces_all_tracked_bytes(self):
        before = {p.name:p.read_bytes() for p in (DATA/'data').iterdir()}
        with tempfile.TemporaryDirectory() as work:
            copy = Path(work)/'31381_made'
            shutil.copytree(DATA, copy, ignore=shutil.ignore_patterns('__pycache__'))
            for _ in range(2):
                subprocess.run([sys.executable, '-I', str(copy/'producecase.py')], check=True, capture_output=True, timeout=10)
                self.assertEqual(before, {p.name:p.read_bytes() for p in (copy/'data').iterdir()})
        self.assertEqual(42, len(before))
        reference = module_at('reference_31381', DATA/'samplecode.py')
        generator = module_at('generator_31381', DATA/'producecase.py')
        for good in ('', '\n', '  \t甲甲é\u2028\n', 'a\r\n'):
            self.assertTrue(generator.valid(good))
            self.assertIsNone(check_31381(good))
        for bad in ('a\nb', 'a\n\n', 'a\rb', '\ra'):
            self.assertFalse(generator.valid(bad))
            self.assertIsNotNone(check_31381(bad))
        inputs = []
        for path in (DATA/'data').glob('*.in'):
            text = path.read_text(); inputs.append(text)
            self.assertTrue(generator.valid(text))
            self.assertIsNone(check_31381(text))
            output = path.with_suffix('.out').read_text()
            self.assertEqual(sorted(text[:-1]), sorted(output[:-1]))
            self.assertEqual(sorted(text[:-1]), sorted(reference.solve(text)))
        self.assertEqual(21, len(set(inputs)))
        self.assertTrue(any(text.startswith(' ') and text.endswith(' \n') for text in inputs))
        self.assertTrue(any('\t' in text for text in inputs))
        self.assertTrue(any('甲' in text for text in inputs))

    def test_actual_catalog_accepts_permutations_and_rejects_common_errors(self):
        prefix = 's = input()\n'
        for program in ('print(s)', 'print(s[::-1])', "print(''.join(sorted(s)))"):
            with self.subTest(program=program):
                self.assertEqual('Accepted', judge.judge('practice', '31381', 'python', prefix+program)['status'])
        for program in ("print(s + '~')", "print(chr(ord(s[0]) ^ 1)+s[1:] if s else '~')",
                        "print(s[1:] if s else '~')", 'print(s.strip())',
                        "print(''.join(sorted(set(s))))", "print(s + '\\n')"):
            with self.subTest(program=program):
                self.assertEqual('Wrong Answer', judge.judge('practice', '31381', 'python', prefix+program)['status'])
        sample = (DATA/'data/0.in').read_text()
        result = judge.run_sample('practice', '31381', 'python', prefix+'print(s[::-1])', sample)
        self.assertEqual('OK', result['status'])
        self.assertTrue(result['checker']['ok'])

    @unittest.skipUnless(shutil.which('g++'), '缺少g++')
    def test_cpp_permutation_through_actual_catalog(self):
        source = '#include <iostream>\n#include <string>\nint main(){std::string s;std::getline(std::cin,s);std::cout<<s<<"\\n";}\n'
        self.assertEqual('Accepted', judge.judge('practice', '31381', 'cpp', source)['status'])
