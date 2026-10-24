"""早期审核遗留的明确题面违规：小域穷举及最小修复，不读取抓取数据。"""
import ast
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from gmyhf_review_fixes import repair_input


def reference(number):
    proof=json.loads((ROOT/f'collab/gmyhf-{number}-authored-admin-review.json').read_text())['entries'][0]['authored_reference']
    source=proof['source'];assert hashlib.sha256(source.encode()).hexdigest()==proof['sha256']
    tree=ast.parse(source);tree.body=[v for v in tree.body if isinstance(v,(ast.Import,ast.ImportFrom,ast.FunctionDef))]
    ns={};exec(compile(tree,'<已审核自产参考>','exec'),ns)
    return ns[proof['function']]


class EarlySemanticTests(unittest.TestCase):
    def test_group_prefixes_keep_both_groups_and_parent_links(self):
        a=[[i,-1 if i==0 else i-1,6,1] for i in range(1001)]
        b=[[0,-1,8,1],[1,0,1,1]]
        text='1001 2\n'+'\n'.join(' '.join(map(str,row)) for row in a+b)+'\n'
        fixed=repair_input(18076,text.encode());values=list(map(int,fixed.split()))
        self.assertEqual([999,2],values[:2]);self.assertEqual(list(itertools.chain.from_iterable(a[:999]+b)),values[2:])
        self.assertIs(fixed,repair_input(18076,fixed))
        invalid=text.replace('1 0 6 1','1 1 6 1',1)
        with self.assertRaises(AssertionError):repair_input(18076,invalid.encode())

    def test_entropy_adjusts_only_largest_cell_with_exact_sum(self):
        given=b'3\r\n0.2 0.3 0.4999999999999999\r\n';fixed=repair_input(18209,given)
        self.assertEqual(b'3\r\n0.2 0.3 0.5000000000000000\r\n',fixed)
        self.assertEqual(Decimal(1),sum(map(Decimal,fixed.decode().split()[1:])))
        self.assertIs(fixed,repair_input(18209,fixed))
        # 精度须按原数值长度设置，不能默认28位丢失尾部误差。
        given=('3\n0.2 0.3 0.'+'4'+'9'*78+'\n').encode()
        fixed=repair_input(18209,given)
        self.assertEqual(Fraction(1),sum(map(lambda x:Fraction(x.decode()),fixed.split()[1:])))
        for bad in (b'3 0.2 0.3 0.4',b'2 0.5 0.5',b'3 NaN 0.5 0.5',b'3 -0.1 0.5 0.6'):
            with self.assertRaises(AssertionError):repair_input(18209,bad)

    def test_drawdown_short_input_gets_neutral_suffix_sample_preserved(self):
        given=b'1% -1% '+b'0% '*8
        fixed=repair_input(20004,given)
        self.assertEqual(given.split()+[b'0%'],fixed.split())
        self.assertIs(fixed,repair_input(20004,fixed))
        sample=b'3.5407% -7.1619% -6.8417% -5.6495% 9.0260% 7.7859% -0.6648% -0.8765% -0.5759% -7.8740%\r\n'
        self.assertIs(sample,repair_input(20004,sample))
        for bad in (b'',b'1',b'a%'):
            with self.assertRaises(AssertionError):repair_input(20004,bad)

    def test_pedestrian_changes_only_zero_lengths(self):
        self.assertEqual(b'3\n-5 1\n0 2\n7 1\n',repair_input(20103,b'3\n-5 0\n0 2\n7 0'))
        given=b'2\r\n-5 1\r\n0 2\r\n';self.assertIs(given,repair_input(20103,given))
        for bad in (b'2\n0 1\n0 2',b'1\n2 -1',b'2\n0 1'):
            with self.assertRaises(AssertionError):repair_input(20103,bad)

    def test_brick_distinctness_is_nearest_strict_increase(self):
        self.assertEqual(b'6 100\n1 2 3 5 6 7\n',repair_input(21727,b'6 100\n1 1 2 5 5 5'))
        given=b'3 100\r\n1 4 99\r\n';self.assertIs(given,repair_input(21727,given))
        for bad in (b'3 100\n1 3 2',b'2 100\n0 1',b'2 1001\n1 2'):
            with self.assertRaises(AssertionError):repair_input(21727,bad)

    def test_waiting_preserves_first_occurrences_and_all_time_bytes(self):
        given=b'5\r\n  10 20 30 40 50\r\n 3 3 5 3 5\r\n'
        expected=b'5\r\n  10 20 30 40 50\r\n 3 1 5 2 4\r\n'
        self.assertEqual(expected,repair_input(21728,given))
        self.assertIs(expected,repair_input(21728,expected))
        for bad in (b'2\n1 2\n0 1',b'2\n1 2\n1 3',b'2\n-1 2\n1 2'):
            with self.assertRaises(AssertionError):repair_input(21728,bad)

    def test_pedestrian_reference_against_all_interval_subsets(self):
        solve=reference(20103)
        for lengths in itertools.product((1,2,3),repeat=5):
            positions=(-5,-2,0,3,7);intervals=[(p-l,p+l) for p,l in zip(positions,lengths)];best=0
            for mask in range(1<<5):
                selected=[i for i in range(5) if mask>>i&1]
                if any(any(a<=p<=b for j,p in enumerate(positions) if j!=i) for i in selected for a,b in [intervals[i]]):continue
                if any(not (intervals[i][1]<intervals[j][0] or intervals[j][1]<intervals[i][0]) for i,j in itertools.combinations(selected,2)):continue
                best=max(best,len(selected))
            text='5\n'+'\n'.join(f'{p} {l}' for p,l in zip(positions,lengths))
            self.assertEqual(str(best),solve(text))

    def test_bricks_reference_against_all_subset_weights(self):
        solve=reference(21727)
        for values in itertools.combinations(range(1,9),4):
            for capacity in range(1,15):
                best=max(len(sub) for size in range(5) for sub in itertools.combinations(values,size) if sum(sub)<=capacity)
                self.assertEqual(str(best),solve(f'4 {capacity}\n'+' '.join(map(str,values))))

    def test_waiting_reference_against_fifo_simulation(self):
        solve=reference(21728)
        for times in itertools.product((0,1,7),repeat=4):
            for order in itertools.permutations(range(1,5)):
                elapsed=0;wait=0
                for student in order:wait+=elapsed;elapsed+=times[student-1]
                self.assertEqual(f'{wait/4:.2f}',solve('4\n'+' '.join(map(str,times))+'\n'+' '.join(map(str,order))))

    def test_drawdown_reference_against_all_price_pairs(self):
        solve=reference(20004)
        for changes in itertools.product((-10,0,10),repeat=4):
            prices=[];price=Fraction(1)
            for change in changes:price*=Fraction(100+change,100);prices.append(price)
            records=[((prices[i]-prices[j])/prices[i],i,j) for i in range(4) for j in range(i,4)]
            drop=max(row[0] for row in records);start=min(i for value,i,j in records if value==drop)
            span=max(j-start for value,i,j in records if value==drop and i==start) if drop else 0
            with localcontext() as context:
                context.prec=80
                value=-Decimal(drop.numerator)*100/Decimal(drop.denominator) if drop else Decimal('-0.0')
                expected=f'{value:.1f}% {span}'
            self.assertEqual(expected,solve(' '.join(f'{x}%' for x in changes)))
