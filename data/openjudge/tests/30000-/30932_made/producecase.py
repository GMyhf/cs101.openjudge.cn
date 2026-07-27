import random
REFERENCE='# External reference: /practice/30932/statistics/\n# Accepted submission: 52760572\n# Source: http://cs101.openjudge.cn/practice/solution/52760572/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    line = sys.stdin.readline().strip()\n    if not line:\n        return\n    \n    tokens = line.split()\n    n = len(tokens)\n    \n    # 将字符串转换为整数或 None\n    tree = []\n    for token in tokens:\n        if token == "null":\n            tree.append(None)\n        else:\n            tree.append(int(token))\n            \n    result = []\n    level = 0\n    \n    while True:\n        start_idx = (1 << level) - 1      # 2^level - 1\n        end_idx = (1 << (level + 1)) - 2  # 2^(level+1) - 2\n        \n        # 如果当前层的起始位置已经越界，说明没有更多层了\n        if start_idx >= n:\n            break\n            \n        max_val = None\n        # 遍历当前层的所有可能位置\n        for i in range(start_idx, min(end_idx + 1, n)):\n            if tree[i] is not None:\n                if max_val is None or tree[i] > max_val:\n                    max_val = tree[i]\n        \n        # 题目保证第一个元素不是null，且层序遍历连续，所以max_val一定有值\n        if max_val is not None:\n            result.append(str(max_val))\n        else:\n            # 理论上不会出现全为null的情况，但为了严谨加上break\n            break\n            \n        level += 1\n        \n    print(" ".join(result))\n\nif __name__ == "__main__":\n    solve()'
SAMPLE='1 3 2 5 3 null 9\n'
GENERATOR_NAME='g30932'
CPP=False
def g30932(r):
    n=r.randint(1,31); vals=[str(r.randint(-100,100)) if i==0 or r.random()<.8 else "null" for i in range(n)]
    return " ".join(vals)+"\n"

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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
