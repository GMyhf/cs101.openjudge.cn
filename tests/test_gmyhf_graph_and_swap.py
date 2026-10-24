"""图裁剪保持题面协议；Wide Swap独立状态图穷举，不依赖抓取数据。"""
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from gmyhf_review_fixes import repair_input
import repair_gmyhf_review_findings as pipeline
from tests.test_gmyhf_early_semantics import reference
from tests.test_gmyhf_reference_commands import HAS_CPP


def swap_cases():
    cases=[]
    for n in range(2,7):
        states=list(itertools.permutations(range(1,n+1)))
        for k in range(1,n):
            unseen=set(states)
            while unseen:
                root=next(iter(unseen));unseen.remove(root);component={root};stack=[root]
                while stack:
                    state=stack.pop()
                    for i in range(n):
                        for j in range(i+k,n):
                            if abs(state[i]-state[j])!=1:continue
                            changed=list(state);changed[i],changed[j]=changed[j],changed[i];changed=tuple(changed)
                            if changed in unseen:unseen.remove(changed);component.add(changed);stack.append(changed)
                best=min(component)
                cases.extend((n,k,state,best) for state in sorted(component))
    return cases


def wide_cpp_source():
    proof=json.loads((ROOT/'collab/gmyhf-27699-authored-admin-review.json').read_text())['entries'][0]['authored_reference']
    assert hashlib.sha256(proof['source'].encode()).hexdigest()==proof['sha256']
    return proof['source']


def cpp_answers(source,cases):
    driver='\nint main(){int t;std::cin>>t;while(t--){int n,k;std::cin>>n>>k;std::vector<int>a(n);for(int &x:a)std::cin>>x;for(int x:solve_wide(n,k,a))std::cout<<x<<" ";std::cout<<"\\n";}}\n'
    source='#define main original_entry\n'+source+'\n#undef main\n'+driver
    with tempfile.TemporaryDirectory() as work:
        path=Path(work)/'wide.cpp';binary=Path(work)/'wide';path.write_text(source)
        subprocess.run(['g++','-std=c++17','-O2',str(path),'-o',str(binary)],check=True,capture_output=True,timeout=30)
        given=str(len(cases))+'\n'+''.join(f'{n} {k}\n'+ ' '.join(map(str,state))+'\n' for n,k,state,_ in cases)
        run=subprocess.run([str(binary)],input=given.encode(),capture_output=True,check=True,timeout=30)
        return [tuple(map(int,line.split())) for line in run.stdout.decode().splitlines()]


class GraphAndSwapTests(unittest.TestCase):
    def test_parcel_repairs_only_coordinate_above_description_bound(self):
        given=b'4\r\n1 100001 100000 2\r\n';expected=b'4\r\n1 100000 100000 2\r\n'
        self.assertEqual(expected,repair_input(19962,given))
        self.assertIs(expected,repair_input(19962,expected))
        for bad in (b'1\n0',b'2\n1',b'0\n'):
            with self.assertRaises(AssertionError):repair_input(19962,bad)

    def test_parcel_reference_matches_all_candidate_locations(self):
        solve=reference(19962)
        for n in range(1,5):
            for coordinates in itertools.product(range(1,5),repeat=n):
                optimum=min(sum(abs(x-location) for x in coordinates) for location in range(1,5))
                self.assertEqual(str(optimum),solve(str(n)+'\n'+' '.join(map(str,coordinates))))

    def test_graph_keeps_end_and_original_edge_order_without_incoming_start(self):
        text=b'4\na z\na 2 b 7 c 3\nb 2 a 9 z 2\nc 0\n'
        fixed=repair_input(30172,text)
        self.assertEqual(b'4\na z\na 2 b 7 c 3\nb 1 z 2\nc 0\n',fixed)
        self.assertIs(fixed,repair_input(30172,fixed))
        # 不可达结局和不涉及起点的环均是合法输入，不能为了过参考而删环。
        legal=b'4\na z\na 0\nb 1 c 1\nc 1 b 1\n'
        self.assertIs(legal,repair_input(30172,legal))
        with self.assertRaises(AssertionError):repair_input(30172,b'3\na z\na 1 missing 1\nb 0\n')

    def test_graph_crop_keeps_late_end_and_at_most_thousand_nodes(self):
        names=['n'+''.join(chars) for chars in itertools.product('abcde',repeat=5)][:1001]
        text='1002\nstart ending\nstart 2 '+names[0]+' 9 ending 1\n'
        text+='\n'.join(name+' 1 ending 0' for name in names[:1000])+'\n'
        fixed=repair_input(30172,text.encode()).decode().splitlines()
        self.assertEqual('1000',fixed[0]);self.assertEqual('start ending',fixed[1]);self.assertEqual(1001,len(fixed))
        self.assertEqual('start 2 '+names[0]+' 9 ending 1',fixed[2])
        self.assertEqual(names[997]+' 1 ending 0',fixed[-1])

    def test_swap_changes_only_invalid_k_and_rejects_bad_permutations(self):
        given=b'4\t999\r\n 4 2 3 1\r\n';fixed=repair_input(27699,given)
        self.assertEqual(b'4\t3\r\n 4 2 3 1\r\n',fixed)
        self.assertIs(fixed,repair_input(27699,fixed))
        for bad in (b'4 2\n1 1 3 4',b'4 0\n1 2 3 4',b'1 1\n1'):
            with self.assertRaises(AssertionError):repair_input(27699,bad)

    def test_story_reference_matches_all_small_dag_paths_and_cycle_rules(self):
        solve=reference(30172);names=['a','b','c','d'];possible=list(itertools.combinations(range(4),2))
        for mask in range(64):
            graph={u:[] for u in names}
            for i,(u,v) in enumerate(possible):
                if mask>>i&1:graph[names[u]].append((names[v],i-3))
            paths=[]
            def walk(u,score,path):
                if u=='d':paths.append((score,path));return
                for v,w in graph[u]:walk(v,score+w,path+[v])
            walk('a',0,['a'])
            if paths:
                best=max(score for score,_ in paths);route=min(path for score,path in paths if score==best);expected=str(best)+'\n'+' '.join(route)
            else:expected='WRONG INPUT'
            text='4\na d\n'+'\n'.join(u+' '+str(len(graph[u]))+''.join(' '+v+' '+str(w) for v,w in graph[u]) for u in names[:-1])
            self.assertEqual(expected,solve(text))
        self.assertEqual('WRONG INPUT',solve('4\na d\na 1 d 1\nb 1 c 1\nc 1 b 1'))
        self.assertEqual('2\na b d',solve('4\na d\na 2 c 1 b 1\nb 1 d 1\nc 1 d 1'))

    def test_wide_sandbox_scope_does_not_count_preserved_large_pairs(self):
        cases=[{'input':f'/tmp/data/{i}.in','output':f'/tmp/data/{i}.out'} for i in range(20)]
        changed={f'{i}.in' for i in range(5)}
        self.assertEqual(cases[:5],pipeline.verification_cases(27699,cases,changed))
        self.assertIs(cases,pipeline.verification_cases(30172,cases,changed))
        with self.assertRaises(ValueError):pipeline.verification_cases(27699,cases,{'0.in'})
        with self.assertRaises(ValueError):pipeline.verification_cases(27699,cases,{'0.in','1.in','2.in','3.in','absent.in'})

    def test_wide_trusted_recheck_rejects_bad_answers_without_claiming_acceptance(self):
        answer=b'2 1 3\n';result=subprocess.CompletedProcess(['trusted-reference'],0,stdout=b'2\n1\n3\n')
        with patch.object(pipeline.subprocess,'run',return_value=result):
            receipt=pipeline.verify_wide_answer(['trusted-reference'],b'3 2\n2 1 3',answer)
            self.assertTrue(receipt['tokens_match']);self.assertNotIn('status',receipt)
            with self.assertRaises(ValueError):pipeline.verify_wide_answer(['trusted-reference'],b'3 2\n2 1 3',b'1 2 3')
        result=subprocess.CompletedProcess(['trusted-reference'],1,stdout=answer)
        with patch.object(pipeline.subprocess,'run',return_value=result):
            with self.assertRaises(ValueError):pipeline.verify_wide_answer(['trusted-reference'],b'',answer)

    @unittest.skipUnless(HAS_CPP,'本机不能编译并运行C++')
    def test_cpp_swap_matches_all_reachable_permutations(self):
        cases=swap_cases();self.assertEqual(4166,len(cases))
        self.assertEqual([best for _,_,_,best in cases],cpp_answers(wide_cpp_source(),cases))
