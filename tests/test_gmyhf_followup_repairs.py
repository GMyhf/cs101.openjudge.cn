"""绑定新修正的数据、整数定义及题面约定；不依赖后台下载缓存。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import gmyhf_followup_repairs as fixes
import gmyhf_input_repairs as replay
import t028_phase2_round23 as round23
import t028_phase2_round20 as round20
import sync_gmyhf_followup as platform
from build_input_domains import statement_text
from check_gmyhf_remaining import expressions, part_routes, lattice_graph_check


class FollowupRepairTests(unittest.TestCase):
    def test_platform_form_preserves_raw_html_and_unchecked_file_controls(self):
        page = '''<form action="/api/global-problem/modify/" method="post">
          <input name="problemId" value="20102" type="hidden">
          <input name="privacy" value="public" type="radio" checked="checked">
          <input name="privacy" value="private" type="radio">
          <input name="filenames[1.in]" value="0" type="hidden">
          <input name="filenames[1.in]" value="1" type="checkbox">
          <input name="token" value="不应保留" type="hidden">
          <select name="language"><option value="en_US">English</option>
            <option value="zh_CN" selected="selected">中文</option></select>
          <textarea name="description"><p>图示<img src="a.png" /></p></textarea>
          <textarea name="input">0<p<=1000\r\n&lt;input name="fake" value="不能成为控件"&gt;</textarea>
        </form>'''
        fields = platform.parse_form(page)
        self.assertEqual('public', fields['privacy'])
        self.assertEqual('0', fields['filenames[1.in]'])
        self.assertEqual('zh_CN', fields['language'])
        self.assertEqual('<p>图示<img src="a.png" /></p>', fields['description'])
        self.assertEqual('0<p<=1000\r\n&lt;input name="fake" value="不能成为控件"&gt;', fields['input'])
        self.assertNotIn('fake', fields)
        self.assertNotIn('token', fields)
        self.assertEqual(platform.normalized(fields), platform.normalized(
            {k: v.replace('\r\n', '\n') for k, v in fields.items()}))
        with self.assertRaises(ValueError): platform.parse_form('<form action="/login/"></form>')

    def test_integer_extrema_only_uses_integer_positions(self):
        self.assertEqual('3 1', fixes.integer_extrema('1 3\n2 -3 1\n'))
        self.assertEqual('-1 -3', fixes.integer_extrema('1 3\n-2 3 -1\n'))
        self.assertEqual('1000000000000000 0', fixes.integer_extrema(
            '1 1000000000\n1000 0 1000\n'))
        self.assertEqual('0 -2997000000000000000', fixes.integer_extrema(
            '3000 1000000000\n'+'1000 -1000000000 -1000\n'*3000))
        rng = random.Random(28912)
        for _ in range(500):
            n, bound = rng.randrange(1, 9), rng.randrange(1, 20)
            terms = [(rng.randrange(-8, 9), rng.randrange(-30, 31), rng.randrange(-6, 7))
                     for _ in range(n)]
            source = f'{n} {bound}\n'+'\n'.join(' '.join(map(str, row)) for row in terms)
            values = [sum(c*abs(a*x+b) for a, b, c in terms) for x in range(bound+1)]
            expected = f'{max(values)} {min(values)}'
            self.assertEqual(expected, fixes.integer_extrema(source), source)
            self.assertEqual(expected, fixes.integer_candidates(source), source)

    def test_route_ties_use_input_numbers_instead_of_names(self):
        source = '1 1 1\nZ 0 0\nA 0 0\nB 0 0\n'
        self.assertEqual('Z A B\n100.00', fixes.route_answer(source))
        self.assertTrue(round23.valid(30281, source))
        self.assertFalse(round23.valid(30281, source.replace('B 0 0', 'A 0 0')))
        self.assertFalse(round23.valid(30281, source.replace('1 1 1', '0.09 1 1')))
        # 题面允许0.1这个边界，Decimal不能与浮点0.1作下界比较。
        self.assertTrue(round23.valid(30281, source.replace('1 1 1', '0.1 1 1')))
        self.assertFalse(round23.valid(30281, source.replace('1 1 1', 'NaN 1 1')))
        self.assertFalse(round23.valid(30281, source.replace('1 1 1', 'x 1 1')))

    def test_reverse_diagonals_against_independent_grid_dijkstra(self):
        source = '8 8 1\na 2 0\nb 4 0\nc 6 0\n'
        self.assertTrue(lattice_graph_check(source))
        routes = part_routes(source)
        best_cost = min(cost for cost, names in routes)
        self.assertEqual(f'{best_cost:.2f}', fixes.route_answer(source).split()[-1])
        self.assertEqual(2, round23._route_cost((8, 8, 1), [(2, 0)]*3, (0, 1, 2))-100)

    def test_repaired_pairs_bind_input_answer_and_replay(self):
        ledger = json.loads((ROOT / 'collab/gmyhf-followup-repairs.json').read_text())
        self.assertEqual(11, len(ledger['entries']))
        table = replay.load_repairs()
        for entry in ledger['entries']:
            with self.subTest(problem=entry['global_number'], file=entry['original_input']):
                before = entry['before_input'].encode(), entry['before_output'].encode()
                after = (ROOT / entry['input']).read_bytes(), (ROOT / entry['output']).read_bytes()
                for prefix, pair in [('before_', before), ('', after)]:
                    self.assertEqual(entry[prefix+'input_sha256'], hashlib.sha256(pair[0]).hexdigest())
                    self.assertEqual(entry[prefix+'output_sha256'], hashlib.sha256(pair[1]).hexdigest())
                number = entry['global_number']
                answer = expressions(after[0].decode()) if number == 30162 else fixes.route_answer(after[0].decode())
                self.assertEqual(answer.split(), after[1].decode().split())
                for pair in (before, after):
                    result = replay.repair_pair(number, entry['original_input'], *pair, table)
                    self.assertEqual(after, result[:2])
                with self.assertRaises(ValueError):
                    replay.repair_pair(number, entry['original_input'], before[0]+b'0', before[1], table)

    def test_expression_repair_keeps_wrong_math_without_assignment(self):
        entry = next(e for e in json.loads((ROOT / 'collab/gmyhf-followup-repairs.json').read_text())['entries']
                     if e['global_number'] == 30162)
        fixed = fixes.expression_input(entry['before_input'].encode())
        self.assertEqual(entry['corrected_input'].encode(), fixed)
        self.assertNotIn(b'=', fixed)
        self.assertIn('WRONG', expressions(fixed.decode()))
        with self.assertRaises(ValueError):
            fixes.expression_input(b'0\n')

    def test_clarifications_are_visible_in_mirrored_statements(self):
        requirements = {20075: ('坐标从1开始', '1 <= x <= n'),
                        30274: ('必须持续操作', '不能提前停止'),
                        30363: ('x < y',), 18104: ('非负整数', '允许为0'),
                        20102: ('非负整数n', 'n=0'), 30281: ('比较编号序列', '不比较零件名称')}
        for number, phrases in requirements.items():
            text = statement_text('practice', str(number))
            for phrase in phrases:
                self.assertIn(phrase, text, number)
        page = (ROOT / 'data/openjudge/pages/practice__20102.html').read_text()
        sample = re.search(r'<dt>样例输入</dt>\s*<dd><pre>(.*?)</pre>', page, re.S)[1].split()
        self.assertEqual(int(sample[0]), len(sample)-1)
        spec = importlib.util.spec_from_file_location('cookie_contract',
            ROOT/'data/openjudge/tests/10000-19963/18104_made/producecase.py')
        copied = importlib.util.module_from_spec(spec);spec.loader.exec_module(copied)
        for module in (round20, copied):
            self.assertTrue(module.valid(18104, '0 1\n0 1\n'))
            self.assertFalse(module.valid(18104, '-1\n1\n'))
            self.assertFalse(module.valid(18104, '101\n1\n'))

    def test_references_and_standalone_generators_remain_consistent(self):
        for number, bucket in [(28912, '20000-29982'), (30281, '30000-')]:
            directory = ROOT / f'data/openjudge/tests/{bucket}/{number}_made'
            spec = importlib.util.spec_from_file_location(f'followup_{number}', directory/'producecase.py')
            module = importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            self.assertEqual((directory/'samplecode.py').read_text(), module.REFERENCE)
            with tempfile.TemporaryDirectory() as temporary:
                subprocess.run([sys.executable, str(directory/'producecase.py')], cwd=temporary,
                               check=True, capture_output=True, timeout=60)
                for path in (Path(temporary)/'data').glob('*'):
                    self.assertEqual((directory/'data'/path.name).read_bytes(), path.read_bytes(), str(path))
            for path in (directory/'data').glob('*.in'):
                expected = fixes.integer_candidates(path.read_text()) if number == 28912 else fixes.route_answer(path.read_text())
                self.assertEqual(expected.split(), path.with_suffix('.out').read_text().split())

    def test_current_28912_data_has_integer_answers_and_valid_inputs(self):
        directory = ROOT/'data/openjudge/tests/20000-29982/28912_GMyhf'
        spec = importlib.util.spec_from_file_location('integer_contract', directory.parent/'28912_made/producecase.py')
        module = importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        files = list((directory/'data').glob('*.in'))
        self.assertEqual(20, len(files))
        for path in files:
            text = path.read_text()
            self.assertTrue(module.valid(28912, text))
            self.assertEqual(fixes.integer_candidates(text), fixes.integer_extrema(text))
            self.assertEqual(fixes.integer_candidates(text).split(), path.with_suffix('.out').read_text().split())


if __name__ == '__main__':
    unittest.main()
