import random
REFERENCE='# External reference: /practice/30936/statistics/\n# Accepted submission: 52760548\n# Source: http://cs101.openjudge.cn/practice/solution/52760548/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\nfrom collections import deque\n\ndef solve():\n    # 读取输入\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    N = int(input_data[0])\n    \n    # 初始化牌堆，将 1 到 N 依次放入双端队列\n    q = deque(range(1, N + 1))\n    result = []\n    \n    # 模拟发牌过程\n    while q:\n        # 步骤1：取出最顶上的一张牌亮出来\n        top_card = q.popleft()\n        result.append(str(top_card))\n        \n        # 步骤2：如果牌堆不空，把新的最顶上的牌移到最底下\n        if q:\n            next_card = q.popleft()\n            q.append(next_card)\n            \n    # 输出结果\n    print(" ".join(result))\n\nif __name__ == "__main__":\n    solve()'
SAMPLE='7\n'
GENERATOR_NAME='g30936'
CPP=False
import re
def valid(text):
    """题面约束：一行一个整数 N（1<=N<=100000）。"""
    if text.endswith('\n'):
        text = text[:-1]
    if not re.fullmatch(r'[1-9][0-9]*', text):
        return False
    return 1 <= int(text) <= 100000

def build_cases():
    r = random.Random(30936)
    ns = [1, 2, 3, 4, 5, 6, 8, 9, 15, 16, 17, 31, 32, 33, 100, 1000, 1023, 1024, 1025,
          4095, 4096, 65535, 65536, 65537, 99999, 100000, 50000, 77777]
    while len(ns) < 39:
        v = r.randint(10000, 100000)
        if v not in ns and v != 7:
            ns.append(v)
    return [SAMPLE] + [f"{n}\n" for n in ns]

from pathlib import Path
import subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/('main.cpp' if CPP else 'main.py'); p.write_text(REFERENCE)
        if CPP:
            exe=Path(d)/'main'; c=subprocess.run(['g++','-O2','-std=c++17',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise SystemExit(c.stderr)
            cmd=[str(exe)]
        else: cmd=[sys.executable,str(p)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=build_cases()
    assert cases[0]==SAMPLE
    assert len(set(cases))==len(cases), "存在重复测试组"
    for i,c in enumerate(cases):
        assert valid(c), f"第 {i} 组不满足题面约束"
        (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
