"""早期数据的观察、比例、数组配对、声明行数和有效排名；自产夹具离线验证。"""
from fractions import Fraction
import itertools
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from gmyhf_review_fixes import repair_input
from tests.test_gmyhf_early_semantics import reference


class EarlyStructureTests(unittest.TestCase):
    def test_outing_removes_only_last_insider_and_preserves_outsiders(self):
        given=b'3\r\n 4 2 1 4 3 5\r\n';fixed=repair_input(23554,given)
        self.assertEqual(b'3\r\n 4 2 1 4  5\r\n',fixed)
        self.assertIs(fixed,repair_input(23554,fixed))
        with self.assertRaises(AssertionError):repair_input(23554,b'3\n1 1 4')
        with self.assertRaises(AssertionError):repair_input(23554,b'3\n1 2')

    def test_plank_scaling_preserves_positive_height_and_speed_order(self):
        given=b'99999 9999 5\n2000 3000 4000 5000 6000\n'
        fixed=repair_input(25580,given);parts=fixed.split()
        self.assertEqual([b'99999',b'999',b'5'],parts[:3])
        self.assertEqual([Fraction(x.decode())/10 for x in given.split()[3:]],[Fraction(x.decode()) for x in parts[3:]])
        self.assertIs(fixed,repair_input(25580,fixed))
        # 1000严格越界，多位缩放及L=0不能遗漏。
        self.assertEqual(b'100 0 1\n100.0\n',repair_input(25580,b'100 0 1\n1000\n'))
        self.assertEqual(b'100 0 1\n100.0001\n',repair_input(25580,b'100 0 1\n100000.1\n'))
        for bad in (b'100 99 1\n1',b'100 0 2\n1 1',b'100 0 1\n0'):
            with self.assertRaises(AssertionError):repair_input(25580,bad)

    def test_assist_keeps_original_pair_offsets(self):
        n=203;hp=list(range(1001,1001+n));times=list(range(1,n+1))
        given=(str(n)+'\n'+' '.join(map(str,hp))+'\n'+' '.join(map(str,times))+'\n').encode()
        fixed=repair_input(27307,given);v=list(map(int,fixed.split()))
        self.assertEqual([200]+hp[:200]+times[:200],v)
        self.assertIs(fixed,repair_input(27307,fixed))
        with self.assertRaises(AssertionError):repair_input(27307,b'1\n5\n0')

    def test_quantum_removes_only_undeclared_last_line(self):
        original=b'2000 10000\r\n'+b'1 '*1999+b'1\r\n'+b'1 2\r\n'*10000
        self.assertEqual(original,repair_input(30222,original+b'2 1\r\n'))
        self.assertIs(original,repair_input(30222,original))
        with self.assertRaises(AssertionError):repair_input(30222,b'2 1\n1 1\n1 2\n2 1\n')

    def test_document_rank_changes_only_rank_token(self):
        given=b'alpha\r\n2\r\n 9 \r\nalpha beta alpha\r\nbeta gamma\r\n'
        expected=given.replace(b' 9 ',b' 3 ')
        self.assertEqual(expected,repair_input(31193,given))
        self.assertIs(expected,repair_input(31193,expected))
        for bad in (b'a\n1\n0\nx\n',b'a\n1\n1\n\n',b'a\n2\n1\nx\n'):
            with self.assertRaises(AssertionError):repair_input(31193,bad)

    def test_outing_reference_against_direct_counts(self):
        solve=reference(23554)
        for observations in itertools.product(range(1,6),repeat=4):
            if len(set(x for x in observations if x<=3))!=sum(x<=3 for x in observations):continue
            missing=[x for x in range(1,4) if x not in observations];outside=sorted(x for x in observations if x>3)
            if not missing or not outside:continue
            expected=' '.join(map(str,missing))+'\n'+' '.join(map(str,outside))
            self.assertEqual(expected,solve('3\n'+' '.join(map(str,observations))))

    def test_plank_reference_against_each_candidate_height(self):
        solve=reference(25580)
        for n in range(1,7):
            velocities=list(range(10,10+n))
            for length in range(6):
                heights=sorted(Fraction(100)-5*(Fraction(length,v))**2 for v in velocities)
                # 阻挡一个小球恰需h达到对应阈值，选择第floor(n/2)+1小阈值。
                h=heights[n//2]
                self.assertEqual(f'{float(h):.2f}',solve(f'100 {length} {n}\n'+' '.join(map(str,velocities))))

    def test_assist_reference_against_all_subsets(self):
        solve=reference(27307)
        for hp in itertools.product((1,3,7),repeat=4):
            for times in itertools.product((1,2),repeat=4):
                costs=[sum(hp[i] for i in range(4) if mask>>i&1) for mask in range(16) if sum(times[i]+1 for i in range(4) if mask>>i&1)>=4]
                self.assertEqual(str(min(costs)),solve('4\n'+' '.join(map(str,hp))+'\n'+' '.join(map(str,times))))

    def test_quantum_reference_against_schedule_dp(self):
        solve=reference(30222)
        possible=list(itertools.combinations(range(1,5),2))
        for mask in range(1<<6):
            edges=[edge for i,edge in enumerate(possible) if mask>>i&1]
            done={};times=(1,5,2,4)
            for node in range(1,5):done[node]=times[node-1]+max((done[u] for u,v in edges if v==node),default=0)
            text=f'4 {len(edges)}\n1 5 2 4\n'+'\n'.join(f'{u} {v}' for u,v in edges)
            self.assertEqual(str(max(done.values())),solve(text))
        self.assertEqual('-1',solve('3 2\n1 1 1\n2 3\n3 2'))
        self.assertEqual('-1',solve('1 1\n1\n1 1'))

    def test_document_reference_counts_repeated_words_once_per_line(self):
        solve=reference(31193)
        for words in itertools.product(('a','b','z'),repeat=4):
            rows=[' '.join(words[:2]),' '.join(words[2:])];counts={w:words.count(w) for w in set(words)}
            for word in ('a','b','q'):
                lines=[str(i+1) for i,row in enumerate(rows) if word in row.split()]
                for rank in range(1,len(counts)+1):
                    expected=(' '.join(lines) or '-1')+'\n'+str(sorted(counts.values(),reverse=True)[rank-1])
                    self.assertEqual(expected,solve(word+'\n2\n'+str(rank)+'\n'+'\n'.join(rows)))
