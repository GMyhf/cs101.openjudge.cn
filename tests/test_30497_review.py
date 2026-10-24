"""30497审核必须读取提示，并区分输入语义与生成器的末尾LF要求。"""
from pathlib import Path
import re
import unittest

import judge
from scripts import audit_gmyhf_30497 as audit

ROOT = Path(__file__).resolve().parents[1]
FIELDS = {'output': '能铺满输出YES，否则NO',
          'hint': '如果你认为此类问题是不可判定的，请在所有样例下输出"undecidable"。（不包含引号）'}


class Review30497Tests(unittest.TestCase):
    def test_hint_must_explicitly_permit_the_constant_response(self):
        self.assertEqual('1 <= N <= 100。 数据范围',
                         audit.plain('1 <= N <= 100。<br />\r\n数据范围'))
        self.assertEqual('undecidable', audit.permitted_hint_response(FIELDS))
        encoded = {'hint': FIELDS['hint'].replace('"', '&quot;')}
        self.assertEqual('undecidable', audit.permitted_hint_response(encoded))
        for fields in ({}, {'output': FIELDS['hint']}, {'hint': 'undecidable'},
                       {'hint': FIELDS['hint'].replace('undecidable', 'YES')}):
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                audit.permitted_hint_response(fields)

    def test_domain_accepts_eof_but_checks_rows_and_bounds(self):
        given = b'1\n0 1000 0 1000'
        expected = {'n': 1, 'min_color': 0, 'max_color': 1000}
        for suffix in (b'', b'\n', b'\r\n'):
            self.assertEqual(expected, audit.input_domain(given + suffix))
        self.assertEqual(100, audit.input_domain(b'100\n' + b'0 0 0 0\n' * 100)['n'])
        invalid = (b'', b'0', b'101\n' + b'0 0 0 0\n' * 101,
                   b'1\n0 0 0', b'1\n0 0 0 0 0', b'2\n0 0 0 0',
                   b'1\n0 0 0 0\n0 0 0 0', b'1\n1001 0 0 0',
                   b'1\n-1 0 0 0', b'1\nx 0 0 0', b'1\n0.0 0 0 0',
                   b'1 1\n0 0 0 0')
        for payload in invalid:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                audit.input_domain(payload)

    def test_pair_requires_permitted_gold_and_valid_input(self):
        given = b'1\n0 0 0 0'
        self.assertEqual(1, audit.verify_pair(FIELDS, given, b'undecidable')['n'])
        audit.verify_pair(FIELDS, given, b'undecidable\r\n')
        for gold in (b'YES', b'NO', b'', b'Undecidable', b'undecidable extra'):
            with self.subTest(gold=gold), self.assertRaises(ValueError):
                audit.verify_pair(FIELDS, given, gold)
        with self.assertRaises(ValueError):
            audit.verify_pair({}, given, b'undecidable')
        with self.assertRaises(ValueError):
            audit.verify_pair(FIELDS, b'1\n1001 0 0 0', b'undecidable')

    def test_current_page_made_data_and_actual_judge(self):
        page = (ROOT / 'data/openjudge/pages/practice__30497.html').read_text()
        fields = {'hint': re.search(r'<dt>提示</dt>\s*<dd>(.*?)</dd>', page, re.S)[1]}
        directory = ROOT / 'data/openjudge/tests/30000-/30497_made'
        paths = list((directory / 'data').glob('*.in'))
        self.assertEqual(40, len(paths))
        for path in paths:
            audit.verify_pair(fields, path.read_bytes(), path.with_suffix('.out').read_bytes())
        result = judge.judge('practice', '30497', 'python', (directory / 'samplecode.py').read_text())
        self.assertEqual('Accepted', result['status'])
        for answer in ('YES', 'NO'):
            self.assertEqual('Wrong Answer', judge.judge('practice', '30497', 'python',
                                                       f'print({answer!r})\n')['status'])


if __name__ == '__main__':
    unittest.main()
