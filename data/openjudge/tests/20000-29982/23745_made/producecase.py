import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/23745/\n# Accepted submission: 52740135\n# Source: http://cs101.openjudge.cn/practice/solution/52740135/\n# License: not declared on the submission page; no license is inferred.\n\nn = int(input())\norig = list(map(int, input().split()))\ndisc = list(map(int, input().split()))\n\nsum_o = sum(orig)\nsum_d = sum(disc)\n\n# 方案1总价：满足满55-20才减20，否则原价\nif sum_o >= 55:\n    cost1 = sum_o - 20\nelse:\n    cost1 = sum_o\ncost2 = sum_d\n\n# 判断输出\nif cost1 < cost2:\n    print(1)\nelif cost2 < cost1:\n    print(2)\nelse:\n    print(3)'
SAMPLE='3\n20 5 10\n15 3 7\n'
GENERATOR_NAME='g23745'
def g23745(r):
    n=r.randint(1,5); return f"{n}\n"+" ".join(str(r.randint(1,100)) for _ in range(n))+"\n"+" ".join(str(r.randint(1,100)) for _ in range(n))+"\n"

def valid(text):
    """题面：第一行 n（整数，1<=n<=5）；第二行 n 个整数（原价）；第三行 n 个整数（优惠价）。"""
    import re
    lines=text.split('\n')
    if lines and lines[-1]=='': lines.pop()
    if len(lines)!=3: return False
    t=lines[0].split()
    if len(t)!=1 or not re.fullmatch(r'[0-9]+',t[0]): return False
    n=int(t[0])
    if not 1<=n<=5: return False
    for l in lines[1:]:
        t=l.split()
        if len(t)!=n or not all(re.fullmatch(r'-?[0-9]+',v) for v in t): return False
    return True

def _answer(o,d):
    c1=sum(o)-20 if sum(o)>=55 else sum(o); c2=sum(d)
    return 1 if c1<c2 else 2 if c2<c1 else 3

def g_target(r,target,n=None,sum_o=None):
    # 每件优惠价都不高于原价；原价总和不足 55 时优惠价总和严格更低，
    # 避免「没满 55 却选满减」这类题面没说清的情形
    while True:
        k=n or r.randint(1,5)
        o=[r.randint(1,40) for _ in range(k)]
        if sum_o is not None:
            if k*40<sum_o or k>sum_o: k=None; continue
            while sum(o)!=sum_o:
                i=r.randrange(k)
                if sum(o)<sum_o and o[i]<40: o[i]+=1
                elif sum(o)>sum_o and o[i]>1: o[i]-=1
        d=[r.randint(max(1,x-r.randint(0,12)),x) for x in o]
        if sum(o)<55 and sum(d)>=sum(o): continue
        if target is None or _answer(o,d)==target:
            return f"{k}\n"+" ".join(map(str,o))+"\n"+" ".join(map(str,d))+"\n"

def build_cases():
    samples=['4\n20 20 5 10\n15 17 3 7\n','5\n20 5 10 20 15\n15 3 7 10 10\n','4\n20 20 5 10\n15 12 3 5\n']
    plan=[(1,None,None)]*7+[(2,None,None)]*7+[(3,None,None)]*7+[
        (None,1,None),(None,1,None),(2,5,None),(1,5,None),(3,5,None),
        (3,None,55),(1,None,55),(2,None,55),(2,None,54),(2,None,54),
        (2,None,56),(1,None,56),(3,None,56),(None,None,200),(1,4,None)]
    cases=[SAMPLE]+samples+[g_target(random.Random(23745*100+i),t,n,so) for i,(t,n,so) in enumerate(plan)]
    return cases

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=build_cases()
    assert len(cases)==40 and len(set(cases))==40 and all(valid(c) for c in cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
