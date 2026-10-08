import random
REFERENCE="# External reference: /practice/30062/statistics/\n# Accepted submission: 52831617\n# Source: http://cs101.openjudge.cn/practice/solution/52831617/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    # 从标准输入读取所有数据并解析为整数\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    nums = []\n    for token in input_data:\n        try:\n            nums.append(int(token))\n        except ValueError:\n            pass\n            \n    count = 0\n    n = len(nums)\n    \n    def backtrack(start, path):\n        nonlocal count\n        # 如果当前子序列长度大于等于 2，计数加 1\n        if len(path) >= 2:\n            count += 1\n            \n        # 使用集合对当前层级的选择进行去重\n        used = set()\n        for i in range(start, n):\n            # 如果当前元素已经在这一层被使用过，则跳过\n            if nums[i] in used:\n                continue\n            \n            # 判断是否满足非递减条件\n            if not path or nums[i] >= path[-1]:\n                used.add(nums[i])\n                backtrack(i + 1, path + [nums[i]])\n                \n    backtrack(0, [])\n    print(count)\n\nif __name__ == '__main__':\n    solve()"
SAMPLE='4 6 7 7\n'
GENERATOR_NAME='g30062'
CPP=False
import re as _re

def valid(text):
    """题面：一行整数，1 ≤ nums.length ≤ 15，-100 ≤ nums[i] ≤ 100。"""
    if not text.endswith('\n') or text.count('\n') != 1:
        return False
    toks = text[:-1].split(' ')
    if not (1 <= len(toks) <= 15):
        return False
    if not all(_re.fullmatch(r'-?(0|[1-9]\d*)', t) and t != '-0' for t in toks):
        return False
    return all(-100 <= int(t) <= 100 for t in toks)

def g30062(r): return " ".join(str(r.randint(-20, 20)) for _ in range(r.randint(2, 12))) + "\n"

def _fmt(a): return " ".join(map(str, a)) + "\n"

def build_cases():
    r = random.Random(30062)
    cases = [SAMPLE, '4 4 3 2 1\n']
    cases += ['7\n', '-100\n', '5 5\n', '5 4\n', '100 -100\n', '-100 100\n']   # 长度 1、2
    cases.append(_fmt([3] * 15))                                    # 全相等 → 14
    cases.append(_fmt(list(range(-7, 8))))                          # 严格递增 15 → 2^15-16
    cases.append(_fmt(list(range(100, 85, -1))))                    # 严格递减 → 0
    cases.append(_fmt(sorted(r.randint(-100, 100) for _ in range(15))))
    cases.append(_fmt([1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8]))
    cases.append(_fmt([-100, 100] * 7 + [-100]))
    cases.append(_fmt([100] * 8 + [-100] * 7))
    cases.append(_fmt([1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]))
    for t in range(10):                                              # 长度 15，值域各异（重复多/少）
        k = r.choice([2, 3, 5, 10, 201])
        vals = r.sample(range(-100, 101), k)
        cases.append(_fmt([r.choice(vals) for _ in range(15)]))
    for t in range(14):                                              # 随机长度
        cases.append(_fmt([r.randint(-100, 100) if t % 2 else r.randint(-5, 5) for _ in range(r.randint(3, 14))]))
    seen = set(); out = []
    for c in cases:
        if c not in seen: seen.add(c); out.append(c)
    assert len(out) == 40, len(out)   # catalog.json 登记了 0..39 共 40 组
    return out

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
    assert all(valid(c) for c in cases)
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
