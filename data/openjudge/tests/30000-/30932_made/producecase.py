import random
REFERENCE='# External reference: /practice/30932/statistics/\n# Accepted submission: 52760572\n# Source: http://cs101.openjudge.cn/practice/solution/52760572/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    line = sys.stdin.readline().strip()\n    if not line:\n        return\n    \n    tokens = line.split()\n    n = len(tokens)\n    \n    # 将字符串转换为整数或 None\n    tree = []\n    for token in tokens:\n        if token == "null":\n            tree.append(None)\n        else:\n            tree.append(int(token))\n            \n    result = []\n    level = 0\n    \n    while True:\n        start_idx = (1 << level) - 1      # 2^level - 1\n        end_idx = (1 << (level + 1)) - 2  # 2^(level+1) - 2\n        \n        # 如果当前层的起始位置已经越界，说明没有更多层了\n        if start_idx >= n:\n            break\n            \n        max_val = None\n        # 遍历当前层的所有可能位置\n        for i in range(start_idx, min(end_idx + 1, n)):\n            if tree[i] is not None:\n                if max_val is None or tree[i] > max_val:\n                    max_val = tree[i]\n        \n        # 题目保证第一个元素不是null，且层序遍历连续，所以max_val一定有值\n        if max_val is not None:\n            result.append(str(max_val))\n        else:\n            # 理论上不会出现全为null的情况，但为了严谨加上break\n            break\n            \n        level += 1\n        \n    print(" ".join(result))\n\nif __name__ == "__main__":\n    solve()'
SAMPLE='1 3 2 5 3 null 9\n'
GENERATOR_NAME='g30932'
CPP=False
import re
_INT = re.compile(r'(0|-?[1-9][0-9]*)$')
def valid(text):
    """题面约束：一行层序序列（按完全二叉树形态补 null），第一个元素不是 null；
    节点数 1<=n<=10000（这里按 token 总数计，更严）；节点值 -10^9<=val<=10^9。
    结构性：完全二叉树编号下，非空结点的父结点（(i-1)//2）必须非空。"""
    if text.endswith('\n'):
        text = text[:-1]
    if '\n' in text:
        return False
    tok = text.split()
    if not (1 <= len(tok) <= 10000) or tok[0] == 'null':
        return False
    for i, t in enumerate(tok):
        if t == 'null':
            continue
        if not _INT.match(t) or not (-10**9 <= int(t) <= 10**9):
            return False
        if i > 0 and tok[(i - 1) // 2] == 'null':
            return False
    return True

def _tree(r, ntok, p, lo, hi):
    a = [str(r.randint(lo, hi))]
    for i in range(1, ntok):
        a.append(str(r.randint(lo, hi)) if a[(i - 1) // 2] != 'null' and r.random() < p else 'null')
    while a[-1] == 'null':
        a.pop()
    return ' '.join(a) + '\n'

def _spine(r, depth, right):
    idx = {0}; i = 0
    for _ in range(depth):
        i = 2 * i + (2 if right else 1); idx.add(i)
    return ' '.join(str(r.randint(-10**9, 10**9)) if k in idx else 'null' for k in range(i + 1)) + '\n'

def build_cases():
    r = random.Random(30932)
    cases = [SAMPLE]
    cases += ['5\n', '-1000000000\n', '1000000000 -1000000000 1000000000\n', '1 null 2\n',
              '-5 -3 -7 null -1 -2\n', '1 null 2 null null 3 4\n', '0 -1 -1 -2 null null -3\n',
              '7 null 3 null null null 9\n']
    for k in range(20):
        lo, hi = [(-100, 100), (-10**9, 10**9), (-50, -1), (-10**9, -10**9 + 5)][k % 4]
        cases.append(_tree(r, r.randint(2, 40), r.choice([0.6, 0.75, 0.9]), lo, hi))
    cases.append(_tree(r, 1000, 0.85, -1000, 1000))
    cases.append(_tree(r, 1000, 0.7, -10**9, -1))
    cases.append(_spine(r, 12, False))           # 左链，8191 个 token
    cases.append(_spine(r, 12, True))            # 右链
    cases.append(_tree(r, 10000, 1.0, -10**9, 10**9))   # 满 13 层 + 第 14 层部分
    cases.append(_tree(r, 10000, 0.97, -10**9, 10**9))
    cases.append(_tree(r, 10000, 0.9, -10**9, -1))      # 全为负数：最大值初始化为 0 会错
    cases.append(' '.join(['-1000000000'] * 8191) + '\n')
    cases.append(_tree(r, 8191, 1.0, 0, 9))
    # 每层最大值都放在该层最后一个位置
    a = []
    for d in range(13):
        w = 1 << d
        a += [str(r.randint(-10**9, 0)) for _ in range(w - 1)] + [str(10**9 - d)]
    cases.append(' '.join(a) + '\n')
    # 每层最大值都在左边、右半层大量 null
    cases.append(_tree(r, 10000, 0.8, -10**9, 10**9))
    return cases

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
