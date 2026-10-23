"""183题独立核对器的自带边界夹具和小规模穷举交叉检查。"""
import itertools
from collections import Counter,deque
import json
from pathlib import Path
import random
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import check_gmyhf_rest as audit
import report_gmyhf_rest as report
from gmyhf_oracles_basic import exact_airplane

# 预期结果来自手算的小例子；不调用参考解或后台下载，不读取未跟踪数据。
EXAMPLES={
12555:('4\n1 2 3 4\n','1.75 2.50 3.25'),
12556:('aAAbbC\n','(a,3)(b,2)(c,1)'),
12557:('1.10\n1.2\n','1.10'),
12559:('2\n11 113\n','11311 11113'),
12560:('2 2\n1 1\n1 0\n','1 1 1 1'),
16527:('aaaa\naab\n','3'),
16528:('3\n0 0\n0 1\n1 1\n','2'),
16529:('3\n2 1 3\n','300.00'),
16532:('1 1\n2 2\n-1 -1\n10\n','-1'),
18105:('3 0 6 1 5\n','3'),
18106:('2\n','1 2 4 3'),
18107:('2\n1 3\n8 9\n','2 3 -1'),
18109:('baab\n','b 2'),
18146:('1 2\n1 7\n','NO'),
18155:('12\n1 2 3 4\n','YES'),
18156:('10\n4 4 8\n','8'),
18161:('1 2\n2 3\n2 1\n4\n5\n1 1\n6\n','29'),
18164:('3\n2 3 5\n','15'),
18167:('2\nabcabc\nabcab\n','3 5'),
18176:('2 3\n3 4 5\n4 25\n','1.33 14.50'),
18182:('1\n2 1 9\n1 5\n1 4\n','alive'),
18188:('2 2\n1 2\n3 4\n','2 2 2 2'),
18189:('120 2\n','2280'),
18211:('40\n20 80 60 40\n','2'),
18223:('2\n6 6 6 6\n2 3 4 5\n','YES NO'),
18224:('3\n9 20 17\n','0b10100 0o24 0x14 0b10001 0o21 0x11'),
19546:('1\n1.0 2.00 3.0 4.00 5.0 6.00\n','5.00'),
19929:('5 3\n1 2 3 2 1\n5 4 3 4 2\n','13'),
19930:('2 2\n0 2\n0 1\n','2'),
19944:('2\n19000101\n20000101\n','Monday Saturday'),
19952:('2\n1\n2\n','3 8'),
19959:('9\n','130'),
19960:('1 1\n2 2\n3 3\n4 4\n5 5\n6 6\n'*3+'1 2\n3 4\n5 6\nabcdef\n','badcfe'),
19961:('2 4 1\n2 2 4 4\n0 0 0 0\n','8'),
20025:('word 12 1 0\n','12=2^2*3 no no'),
20026:('12\n','12'),
20027:('aaz\n10\n','abk'),
20052:('2 4 1\n2 2 4 4\n0 0 0 0\n','8'),
20074:('2\n170 75 M\n165 45 F\n','1 1'),
20075:('2 2 2\n0 2\n0 1\n1 1\n2 1\n','2 NO'),
20089:('5500\n3 3 3 3 3 3 3\n','2'),
20090:('4\n1\n2\n3\n4\n','1 7 1 3'),
20091:('2\n3\n4\n','3 6'),
20100:('4\n6 6 6\n3 4 5\n1 4 6\n','1'),
20101:('1\nx+2\n','3+(x-1)'),
20106:('1 2 1\n0 3\n0 0 0 1\n','3'),
20107:('1\n1 1\n4 4 10\n','9 0 10'),
20121:('2\n7 5\n3 9\n','7593'),
20122:('1 0421\n0421 0421 0830 1030\n','1'),
20125:('2\n1 1\n','2'),
20127:('2 2\n0 3\n2 1\n','1'),
20134:('10 10 1 2 1\n5 1\n','15.00'),
20136:('2 3\n0 1\n1 0 2\n2 1\n','NO!'),
20140:('[2b[3a]c]\n','baaacbaaac'),
20162:('1\n1 10 7 1\n','7'),
20163:('1\nAlpha Beta meets Gamma .\n','Alpha Beta\nGamma'),
20196:('2020 1 10\n','1441 5 12'),
21458:('6 4\n2 1\n4 7\n3 5\n3 5\n','10'),
21459:('2\n','2/2=1'),
21462:('3\n104 101 109\n97 0 111\n110 100 115\n','handsome'),
21532:('231\n','33'),
21554:('3\n2 1 1\n','2 3 1 1.00'),
21608:('2\n1 : 2\n2 : -1\n','2'),
23421:('3 4\n3000 2000 1500\n4 3 1\n','3500'),
23454:('Boy   next   door\n','Boy next door'),
23558:('3 2 1\n0 1\n1 2\n0\n','0 1'),
23564:('12\n','0'),
23566:('2 2\n1 100\n2 100\n100-20\n200-50\n','150'),
25301:('3\na 3 2\nb 4 1\nc 3 2\n','3 2 a c'),
25302:('1\n2\n1 2\n2 3\n','1'),
25538:('9\n','Yes'),
25561:('2 2\n1:100 2:120\n1:300 2:350\n200-30 400-70\n100-80\n','260'),
25566:('3\n1 2\n4 3\n3 1\n','9'),
25572:('3\n5 5 0\n1 1 0\n0 0 9\n','no'),
26971:('3\n1 0 2\n','5'),
26976:('3\n1 2 3\n','2'),
26977:('3\n2 0 2\n','2'),
26978:('4 2\n1 3 2 4\n','3 3 4'),
26999:('1\naaaa aa\n','0 1 2'),
27018:('3\n2 1 3\n','3'),
27072:('2\n','2'),
27093:('5 3\n7 7 3 6 2\n','6 7 7 2 3'),
27103:('3 2\n1 2 1\n','2'),
27104:('3\n0 1 0\n','1'),
27122:('5 3\n1 2 3 4 7\n','3'),
27141:('3\n520 521 519\n','1560'),
27205:('2 3\n0 0 1\n0 0 0\n','4'),
27256:('5\nadd 1\nadd 2\nquery\ndel\nquery\n','1.5 2'),
27300:('3\nGPT-1B\nBert-2M\nGPT-3M\n','Bert: 2M\nGPT: 3M, 1B'),
27311:('3\n2 0 2\n0 0 0\n','4'),
27312:('2\nGH\n','1'),
27313:('4\n2 0 3 1\n','2'),
27314:('HELLO, hello. WORLD.\nhello hi\n','Hi, hi. World.'),
27363:('5\n1 4 1 5 1\n','2'),
27371:('keyword\n1\nballoon\n','cbizsces'),
27372:('3\nhello\nhell\nhi\n','6'),
27373:('4\n4\n23 9 182 79\n','9182'),
27401:('3 10\n3 5 8\n','11'),
27441:('40 3\n4 5 11\n5 4 1\n','9'),
27598:('3\n2\n1 5 8\n','6'),
27623:('34 12\n15 24\n0 0\n','win lose'),
27625:('4\n','7'),
27626:('20\n','6'),
27631:('1\n3\n10 20 30\n','2'),
27637:('1\nA(B,C)\n','ABC BAC'),
27638:('3\n-1 -1\n0 2\n-1 -1\n','1 2'),
27653:('1 4 1 2\n','3/4'),
27862:('3\n1 2\n1 3\n2\n2 2 1\n3 3 0\n','3 0'),
27925:('1\n1 2\nENQUEUE 1\nENQUEUE 9\nENQUEUE 2\nDEQUEUE\nDEQUEUE\nDEQUEUE\nSTOP\n','1 2 9'),
27928:('4\n7 10 3 6\n10\n6\n3\n','3 6 7 10'),
27947:('1\n3 1 2\n','2 3 2'),
27948:('1\n01\n','BIF'),
27951:('2 4\n1 2 1 3\n','3'),
28012:('3\n0 1\n1 2\n1\n','1'),
28050:('3\n0 0\n','fail'),
28052:('2\n0 0\n0 0\n','2'),
28186:('3 2\n1 4 3\n','3'),
28193:('3 1\n5 2 4\n1 2\n','6'),
28334:('3 1\n0 1\n','2'),
28664:('2\n371311200312247819\n130631197601191234\n','YES NO'),
28674:('5\nLfrjXhnjshj\n','GameScience'),
28700:('MCMXCIV\n','1994'),
28702:('3\n3 2 6\n3 2 8\n3 2 9\n','3 1 0'),
28749:('1 1\nW\n1 1\n','1'),
28914:('1\n0 10 5\n3 7\n','3'),
29256:('5 2\n100 80 90 75 95\n','260'),
29335:('/a/../...//b/./\n','/.../b'),
29646:('1\n1 1\n','1'),
29740:('2 1\n2 0\n0 1\n1 2 3\n','2 5'),
29886:('3 1 4\n','4'),
29896:('20 4\n1 2 5 10\n','5'),
29917:('1\n','1 1.00'),
29918:('10\n',''),
29947:('10 2\n2 4\n4 5\n','7'),
29949:('3 50\n60 10\n100 20\n120 30\n','240.00'),
29950:('arcane\n','5'),
29952:(')((()))((()\n','6'),
29954:('1 3 1\nS#E\n','2'),
29982:('11,35,3\n','12,21,30\n15,24,33\n18,27'),
30102:('4\n1\n3\n2\n4\n','4'),
30158:('1 2\n1 1 0\n5 100\n','8'),
30163:('1\n1 1\n0\n1 1\n','1'),
30178:('2\n1 2\n3 0\n','yes'),
30201:('3\n0 1 2\n1 0 3\n2 3 0\n','6'),
30204:('2 10\n4 1\n3 3\n','4'),
30212:('7 2\n','3'),
30216:('1\n','0 1 1 1'),
30218:('3\n5 10 -5\n','2 5 5'),
30220:('1 1\n-5\n','5'),
30274:('3 4\n1 2 3\n','1'),
30276:('4 5\n','13'),
30283:('2\n0 0 1 2\n0 0 1 1\n','1 4'),
30313:('3 1\n1 2 5\n','0'),
30339:('1 5\nX.X.X\n','2'),
30363:('3 2\n1 2\n2 3\n','1 3'),
30376:('abc\n','1'),
30381:('3 4\n1 2 3\n','3'),
30382:('abbb\nab\n','3'),
30399:('2 2\n2 1\n1 2\n','0 0 0 1 1 0 1 1'),
30442:('1\n3\n2 4 8\n','2'),
30571:('0\n','1'),
30637:('abc\nbca\ncab\n\n','YES NO NO'),
30669:('3 1\n1 2\n2 3\n1 3 1 1\n','1 1'),
30680:('4\n15 2\n2\n8 20\n20\n','8 20 2 15'),
30868:('7 3 5\n4\n4\n10\n13\n41\n','No Yes Yes Yes'),
30887:('3\n1 2 3\n','3'),
30888:('3 2\n10 100\n8 95\n5 80\n','8.900000'),
30889:('3\n- -\n1 L\n1 R\n','2'),
30894:('3\ng 4\nd 8\nc 10\ndc\n110\n','110 dc'),
30901:('1\n3\n1 2 3\n','3'),
30909:('2 2\n1 3\n2 5\n','2'),
30910:('2 2\n1 2 3\n2 1 4\n','7'),
30911:('4 1 3\n','6'),
30912:('3\n2 1 3\n','5 6 3'),
30913:('2 2\n1 2 4\n2 1 4\n1\n','16'),
30942:('TTFF\n2\n','4'),
30943:('3 2\n0 1 1\n1 2 1\n','3'),
30947:('2 3\n2 3\n6\n7\n8\n','Yes No Yes'),
30953:('3 2\n1 3\n3 2\n','1 2 2'),
31086:('2\n1 2 3\n0 0 1\n','KittyPig Piggy'),
31087:('2\n1 2 3\n0 0 1\n','Piggy Piggy'),
31378:('AA\nAAA\n','2 0'),
31418:('3\n3 2 1\n','1'),
}

class RemainingOracleTests(unittest.TestCase):
    def test_summary_requires_complete_and_current_algorithm_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);(root/'collab').mkdir();(root/'scripts').mkdir()
            sources={}
            for name in ['check_gmyhf_rest']+['gmyhf_oracles_'+g for g in report.GROUPS]:
                path=root/'scripts'/f'{name}.py';path.write_text('# 测试夹具\n')
                sources[str(path.relative_to(root))]=report.sha(path)
            directory=root/'data/openjudge/tests/unit/1_GMyhf/data';directory.mkdir(parents=True)
            (directory/'0.in').write_text('1\n');(directory/'0.out').write_text('2\n')
            record={'input':str((directory/'0.in').relative_to(root)),
                    'input_sha256':report.sha(directory/'0.in'),'output_sha256':report.sha(directory/'0.out'),'matches':True}
            (root/'statement').write_text('题面')
            with patch.object(report,'ROOT',root):
                prior={'global_number':1,'title':'夹具','statement':'statement',
                       'statement_sha256':report.sha(root/'statement'),
                       'download_snapshot_sha256':report.bind_files([record],directory)}
                baseline={'entries':[prior],'sources':{},'manual_findings':{}}
                (root/'collab/gmyhf-download-followup.json').write_text(json.dumps(baseline))
                (root/'collab/gmyhf-download-materialize.json').write_text(json.dumps(
                    {'materialized':[{'global_number':1,'bucket':'unit','local_id':'1'}]}))
                evidence={'sources':sources,'entries':[{'global_number':1,'title':'夹具','cases':1,'files':[record]}]}
                self.assertEqual(1,report.build([evidence])['summary']['matching_pairs'])
                for invalid in ([],[evidence,evidence],[{'sources':{},'entries':evidence['entries']}]):
                    with self.assertRaises(ValueError):report.build(invalid)
                record['unproved']='算法异常'
                with self.assertRaises(ValueError):report.build([evidence])
                del record['unproved'];record['matches']='true'
                with self.assertRaises(ValueError):report.build([evidence])
                record['matches']=True;evidence['entries'][0]['cases']=2
                with self.assertRaises(ValueError):report.build([evidence])
                evidence['entries'][0]['cases']=1;(root/'statement').write_text('题面变化')
                with self.assertRaises(ValueError):report.build([evidence])

    def test_evidence_rejects_missing_duplicate_and_stale_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);directory=root/'cases';directory.mkdir()
            (directory/'0.in').write_text('1\n');(directory/'0.out').write_text('2\n')
            record={'input':'cases/0.in','input_sha256':report.sha(directory/'0.in'),
                    'output_sha256':report.sha(directory/'0.out')}
            with patch.object(report,'ROOT',root):
                self.assertEqual(64,len(report.bind_files([record],directory)))
                for records in ([],[record,record]):
                    with self.assertRaises(ValueError):report.bind_files(records,directory)
                (directory/'0.out').write_text('3\n')
                with self.assertRaises(ValueError):report.bind_files([record],directory)
                (directory/'0.out').write_text('2\n');(directory/'0.in').write_text('0\n')
                with self.assertRaises(ValueError):report.bind_files([record],directory)

    def test_all_183_oracles_have_independent_small_examples(self):
        self.assertEqual(183,len(EXAMPLES))
        self.assertEqual(set(EXAMPLES),set(audit.SOLVERS))
        for number,(source,expected)in EXAMPLES.items():
            with self.subTest(problem=number):self.assertEqual(expected.split(),audit.SOLVERS[number](source).split())

    def test_airplane_aggregate_against_exact_seat_blocks(self):
        def partitions(total,minimum=1):
            if total==0:yield ()
            for first in range(minimum,total+1):
                for rest in partitions(total-first,first):yield(first,)+rest
        for total in range(1,10):
            for flocks in partitions(total):
                source=f'1 {len(flocks)}\n'+' '.join(map(str,flocks))+'\n'
                self.assertEqual(exact_airplane(1,flocks),audit.SOLVERS[18146](source)=='YES',flocks)
        # 同一窝的两只可分坐两个四座块，为其他窝留下隔离空位。
        self.assertTrue(exact_airplane(3,[2]*9+[4]))
        self.assertEqual('YES',audit.SOLVERS[18146]('3 10\n'+'2 '*9+'4\n'))
        rng=random.Random(18146)
        for planes in (2,3):
            for _ in range(40):
                flocks=[rng.randrange(1,7)for _ in range(rng.randrange(1,7))]
                source=f'{planes} {len(flocks)}\n'+' '.join(map(str,flocks))
                self.assertEqual(exact_airplane(planes,flocks),audit.SOLVERS[18146](source)=='YES',flocks)

    def test_two_2048_rules_and_exact_recurrence_prefix(self):
        from math import isqrt
        source='2 4 1\n2 2 4 0\n0 0 0 0\n'
        self.assertEqual('8',audit.SOLVERS[19961](source))
        self.assertEqual('4',audit.SOLVERS[20052](source))
        values=[1]
        for _ in range(100):values.append(4*values[-1]+isqrt(11*values[-1]**2))
        source='101\n'+'\n'.join(map(str,range(1,102)))
        self.assertEqual([v%10 for v in values],list(map(int,audit.SOLVERS[20090](source).split())))

    def test_constrained_queue_matches_all_reachable_small_orders(self):
        rng=random.Random(27093)
        for _ in range(45):
            initial=tuple(rng.randrange(5)for _ in range(6));limit=rng.randrange(4);seen={initial};queue=[initial]
            for state in queue:
                for i in range(len(state)-1):
                    if abs(state[i]-state[i+1])<=limit:
                        following=list(state);following[i],following[i+1]=following[i+1],following[i];following=tuple(following)
                        if following not in seen:seen.add(following);queue.append(following)
            source=f'6 {limit}\n'+' '.join(map(str,initial))
            self.assertEqual(min(seen),tuple(map(int,audit.SOLVERS[27093](source).split())))

    def test_rabbit_counts_match_every_order_of_adjacent_swaps(self):
        for n in range(2,7):
            counts=Counter()
            for order in itertools.permutations(range(n-1)):
                state=list(range(n))
                for i in order:state[i],state[i+1]=state[i+1],state[i]
                counts[tuple(state)]+=1
            for permutation in itertools.permutations(range(n)):
                source=str(n)+'\n'+' '.join(map(str,permutation))
                self.assertEqual(counts[permutation],int(audit.SOLVERS[27313](source)))

    def test_lcs_sum_against_literal_pair_enumeration(self):
        for n in range(1,40):
            expected=0
            for a,b in itertools.product(map(str,range(1,n+1)),repeat=2):
                expected+=max([0]+[width for width in range(1,len(a)+1)for i in range(len(a)-width+1)if a[i:i+width]in b])
            self.assertEqual(expected,int(audit.SOLVERS[27072](str(n))))

    def test_perfect_windows_and_equal_sequence_against_enumeration(self):
        rng=random.Random(30102)
        for _ in range(150):
            a=[rng.randrange(1,8)for _ in range(rng.randrange(2,9))];best=0
            for i in range(len(a)):
                for j in range(i+1,len(a)):
                    if a[i]<a[j]and all(a[i]<v<a[j]for v in a[i+1:j]):best=max(best,j-i+1)
            source=str(len(a))+'\n'+' '.join(map(str,a))
            self.assertEqual(best,int(audit.SOLVERS[30102](source)))
            def single_cost(start,target):
                # 有限状态BFS直接使用+2和-1，不套用审核器的代价公式。
                distance={start:0};queue=deque([start])
                while target not in distance:
                    v=queue.popleft()
                    for u in(v+2,v-1):
                        if -3<=u<=12 and u not in distance:distance[u]=distance[v]+1;queue.append(u)
                return distance[target]
            expected=min(sum(single_cost(v,t)for v in a)for t in range(0,10))
            self.assertEqual(expected,int(audit.SOLVERS[30887](source)))

    def test_veto_nim_against_recursive_legal_move_game(self):
        from functools import lru_cache
        @lru_cache(None)
        def win(state):
            if sum(state)==0:return False
            results=[]
            for i,size in enumerate(state):
                for following in range(size):
                    changed=list(state);changed[i]=following;results.append(not win(tuple(changed)))
            return any(results)if len(results)==1 else sum(results)>=2
        for state in itertools.product(range(5),repeat=3):
            if not any(state):continue
            source='1\n'+' '.join(map(str,state))
            self.assertEqual(win(state),audit.SOLVERS[31087](source)=='Piggy')


if __name__=='__main__':unittest.main()
