"""31381逐题SPJ：独立小域、CLI及真实沙箱判题，不依赖后台抓取数据。"""
import importlib.util
import itertools
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import judge
from scripts import index_tests

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT/'data/openjudge/tests/30000-/31381_made/checker.py'
spec = importlib.util.spec_from_file_location('checker_31381', CHECKER)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class PermutationCheckerTests(unittest.TestCase):
    def test_counts_against_independent_sorted_small_domain(self):
        words = [''.join(p) for n in range(5) for p in itertools.product('ab ', repeat=n)]
        for given in words:
            for actual in words:
                self.assertEqual(sorted(given) == sorted(actual), checker.matches(given, actual), (given, actual))
        self.assertTrue(checker.matches('甲甲乙\t\u2028', '\u2028甲\t乙甲'))
        self.assertFalse(checker.matches('é', 'e\u0301'))

    def test_cli_preserves_spaces_line_structure_and_encoding(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work); given = root/'input'; actual = root/'output'
            # 故意没有参考答案文件：本题由输入即可判断，不能依赖错误的后台金标准。
            command = [sys.executable, '-I', str(CHECKER), str(given), str(actual), str(root/'unused')]
            for source, output, wanted in (
                (b'aab\n', b'baa\r\n', 0), (b'aab', b'aba', 0),
                (b' a\t\n', b'\ta \n', 0), ('甲乙甲\n'.encode(), '乙甲甲\n'.encode(), 0),
                (b'\n', b'\r\n', 0), (b'aab\n', b'abb\n', 42),
                (b'aab\n', b'aab~\n', 42), (b'aab\n', b'ab\n', 42),
                (b' a\n', b'a\n', 42), (b'a \n', b'a\n', 42),
                (b'aab\n', b'aab\n\n', 42), (b'aab\n', b'aa\nb', 42),
                (b'aab\n', b'aab\r', 42), (b'aab\n', b'\xff', 42),
                (b'aab\n', b'', 42), (b'\xef\xbf\xbd\n', b'\xff\n', 42),
                (b'x'*(2*1024*1024+1), b'x'*(2*1024*1024+1), 42),
                (b'\xff\n', b'a\n', 3), (b'a\nb\n', b'ab\n', 3)):
                with self.subTest(source_length=len(source), output_length=len(output), wanted=wanted):
                    given.write_bytes(source); actual.write_bytes(output)
                    result = subprocess.run(command, capture_output=True, timeout=5)
                    self.assertEqual(wanted, result.returncode, result.stderr)
                    if wanted: self.assertTrue(result.stdout)

    def test_index_hook_and_six_programs_through_real_judge(self):
        with tempfile.TemporaryDirectory() as work:
            mirror = Path(work); directory = mirror/'tests/31381_made'; directory.mkdir(parents=True)
            shutil.copyfile(CHECKER, directory/'checker.py')
            (directory/'0.in').write_text('aaba\n')
            # 即使金标准不是排列，合法的学生输出仍应通过。
            (directory/'0.out').write_text('不是参考排列\n')
            cases = [{'input':'tests/31381_made/0.in', 'output':'tests/31381_made/0.out'}]
            with patch.object(index_tests, 'MIRROR', mirror): hooks = index_tests.judge_hooks(cases)
            self.assertEqual('tests/31381_made/checker.py', hooks['checker'])
            item = {'book':'t31381', 'id':'31381', 'test_cases':cases, **hooks}
            prefix = 's = input()\n'
            programs = [('print(s)', 'Accepted'), ('print(s[::-1])', 'Accepted'),
                        ("print(''.join(sorted(s)))", 'Accepted'),
                        ("print(s + '~')", 'Wrong Answer'),
                        ('print(chr(ord(s[0]) ^ 1) + s[1:])', 'Wrong Answer'),
                        ('print(s[1:])', 'Wrong Answer'),
                        ("print(s + '\\n')", 'Wrong Answer')]
            original_limits = judge.LIMITS_CACHE
            limits_before = dict(original_limits)
            with patch.object(judge, 'MIRROR', mirror), patch.object(judge, 'catalog_item', return_value=item), patch.object(judge, 'LIMITS_CACHE', {}):
                for program, wanted in programs:
                    with self.subTest(program=program):
                        self.assertEqual(wanted, judge.judge('t31381', '31381', 'python', prefix+program)['status'])
                (directory/'0.in').write_bytes(b'\xff\n')
                self.assertEqual('Judge Error', judge.judge('t31381', '31381', 'python', "print('a')")['status'])
            self.assertIs(judge.LIMITS_CACHE, original_limits)
            self.assertEqual(limits_before, judge.LIMITS_CACHE)
