"""无后台数据的六题：独立算法核答案、拒绝非法输入并复现全部字节。"""
from collections import Counter
import heapq
import importlib.util
import itertools
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
NUMBERS=(27207,29337,29893,29894,31178,31200)


def directory(number):
    return ROOT/'data/openjudge/tests'/('20000-29982' if number<30000 else '30000-')/f'{number}_made'


def load(number):
    spec=importlib.util.spec_from_file_location('generator_'+str(number),directory(number)/'producecase.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def nano_oracle(text):
    """非负超边最短路：某配方全部前体完成后才可候选，不要求先结算所有配方。"""
    values=iter(map(int,text.split()));n=next(values);reverse=[[] for _ in range(n)]
    needed=[];totals=[];owners=[];queue=[]
    for u in range(n):
        for _ in range(next(values)):
            time=next(values);count=next(values);ingredients=Counter(next(values) for _ in range(count))
            index=len(needed);needed.append(len(ingredients));totals.append(time);owners.append(u)
            for v,multiplicity in ingredients.items():reverse[v].append((index,multiplicity))
            if not ingredients:heapq.heappush(queue,(time,u))
    costs={}
    while queue:
        cost,u=heapq.heappop(queue)
        if u in costs:continue
        costs[u]=cost
        if u==0:return str(cost)
        for index,multiplicity in reverse[u]:
            totals[index]+=cost*multiplicity;needed[index]-=1
            if needed[index]==0:heapq.heappush(queue,(totals[index],owners[index]))
    raise ValueError('目标不可达')


def signed_oracle(text):
    lines=text.splitlines();nums=list(map(int,lines[0].split()));target=int(lines[1]);cut=len(nums)//2
    left=Counter(sum(v*sign for v,sign in zip(nums[:cut],signs))
                 for signs in itertools.product((-1,1),repeat=cut))
    return str(sum(left[target-sum(v*sign for v,sign in zip(nums[cut:],signs))]
                   for signs in itertools.product((-1,1),repeat=len(nums)-cut)))


def train_oracle(text):
    a,n,m,x=map(int,text.split())
    # 枚举第二站人数，直接逐站上/下车；生成域内单调搜索会很快找到。
    for second in range(m+1):
        old,new=a,second;aboard=a;answer=a
        for station in range(3,n):
            old,new=new,old+new;aboard+=new-old
            if station==x:answer=aboard
        if aboard==m:return str(answer)
        if aboard>m:break
    raise ValueError('无合法上车人数')


def oracle(number,text):
    if number==27207:return nano_oracle(text)
    if number==29337:return signed_oracle(text)
    if number in (29893,29894):return train_oracle(text)
    if number==31178:return text.removesuffix('\n').removesuffix('\r')
    a,b=map(int,text.split());values=[str(v) for v in (153,370,371,407) if a<=v<=b]
    return ' '.join(values) if values else 'NO'


class MissingNormalDataTests(unittest.TestCase):
    def test_all_answers_and_byte_reproduction(self):
        for number in NUMBERS:
            with self.subTest(number=number),tempfile.TemporaryDirectory() as temporary:
                generator=load(number);generator.build(temporary)
                files=sorted((directory(number)/'data').glob('*'))
                self.assertEqual(42,len(files))
                for path in files:
                    self.assertEqual(path.read_bytes(),(Path(temporary)/path.name).read_bytes())
                for given in (directory(number)/'data').glob('*.in'):
                    text=given.read_text();self.assertTrue(generator.valid(text),given)
                    expected=given.with_suffix('.out').read_text()
                    self.assertEqual(oracle(number,text)+'\n',expected,given)

    def test_invalid_inputs_are_rejected(self):
        invalid={27207:['0\n','1\n0\n','1\n1\n0 1\n0\n',
                         '1\n1\n10001 0\n\n','2\n1\n0 1\n2\n1\n0 0\n\n',
                         '1\n1\n0 1\n\n','1\n1\n0 0\n7\n'],
                 29337:['\n0\n','1\n','1 -1\n0\n','1001\n0\n','1\n1001\n','0 '*21+'\n0\n','600 600\n0\n'],
                 29893:['1 2 1 1\n','5 7 20 4\n','1 1 1 1\n','5 7 31 4\n','5 7 16 4\n','5 7 32 7\n','5 7 32 0\n','5 7 32\n','5 7 -1 4\n'],
                 31178:['','\n','a'*101+'\n','a\nb\n'],
                 31200:['99 999\n','100 1000\n','500 100\n','100\n','100 500 999\n']}
        invalid[29894]=invalid[29893]
        for number,texts in invalid.items():
            generator=load(number)
            for text in texts:
                with self.subTest(number=number,text=text):self.assertFalse(generator.valid(text))

    def test_independent_models_on_small_domains(self):
        target=load(29337).reference.solve
        for length in range(1,5):
            for nums in itertools.product(range(3),repeat=length):
                for goal in range(-sum(nums)-1,sum(nums)+2):
                    text=' '.join(map(str,nums))+f'\n{goal}\n'
                    expected=sum(sum(v*s for v,s in zip(nums,signs))==goal
                                 for signs in itertools.product((-1,1),repeat=length))
                    self.assertEqual(str(expected),target(text))
        narcissus=load(31200).reference.solve
        self.assertEqual([153,370,371,407],[n for n in range(100,1000)
                         if int(narcissus(f'{n} {n}\n')!='NO')])
        train=load(29893)
        for n in range(2,10):
            for a in (0,1,7):
                for second in (0,1,5):
                    counts=train.passengers(a,n,second)
                    for x in range(1,n):
                        text=f'{a} {n} {counts[n-1]} {x}\n'
                        self.assertEqual(str(counts[x]),train.reference.solve(text))
                        self.assertEqual(str(counts[x]),train_oracle(text))


if __name__=='__main__':unittest.main()
