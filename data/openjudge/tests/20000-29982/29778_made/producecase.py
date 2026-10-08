import random
REFERENCE='# External reference: /practice/29778/statistics/\n# Accepted submission: 52682233\n# Source: http://cs101.openjudge.cn/practice/solution/52682233/\n# License: not declared on the submission page; no license is inferred.\n\nc = 0\n\ndef sorting(l):\n    if len(l) == 1:\n        return l\n    global c\n    l1, l2 = sorting(l[:len(l)//2]), sorting(l[len(l)//2:])\n    n = []\n    while l1 or l2:\n        if l1 and l2:\n            if l1[-1] >= l2[-1]:\n                n.append(l1.pop())\n            else:\n                if not 2*l1[0] >= l2[-1]:\n                    l, r = 0, len(l1)\n                    while l < r:\n                        mid = (l + r)//2\n                        if 2*l1[mid] < l2[-1]:\n                            l = mid + 1\n                        else:\n                            r = mid\n                    c += l\n                n.append(l2.pop())\n        elif l1:\n            n.extend(l1[::-1])\n            l1.clear()\n        else:\n            n.extend(l2[::-1])\n            l2.clear()\n    return n[::-1]\n\nsorting([int(input()) for i in range(int(input()))])\nprint(c)'
SAMPLE='10\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n'
GENERATOR_NAME='g29778'

def valid(text):
    """题面契约：第一行 N，1<=N<=100000；其后恰 N 行，每行一个非负整数速度；
    题面明说“速度各不相同”，故要求互异（提示里 5,5 的例子与此矛盾，取更严的一侧）。
    速度上限题面未给。"""
    import re
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    num = re.compile(r'0|[1-9][0-9]*')
    if not all(num.fullmatch(x) for x in lines):
        return False
    n = int(lines[0])
    if not 1 <= n <= 100000 or len(lines) != n + 1:
        return False
    v = lines[1:]
    return len(set(v)) == n

VMAX = 10 ** 6

def _distinct(r, n, hi=VMAX):
    return r.sample(range(0, hi + 1), n)

def g29778(r, idx):
    N = 40000
    if idx == 1: v = [0]
    elif idx == 2: v = [7]
    elif idx == 3: v = [0, 1]                      # 0 被 1 超过且 1 > 0
    elif idx == 4: v = [1, 2]                      # 恰好 2 倍不算
    elif idx == 5: v = [2, 5, 0, 1, 3]
    elif idx <= 14: v = _distinct(r, r.randint(1, 30), r.choice([40, 60, 1000]))
    elif idx <= 20: v = _distinct(r, r.randint(500, 3000))
    # data/ 合计须 <= 10MB：N=100000 满规模只留 21、27（答案最大）、31 三组，其余规模组 N 缩到 3~4 万
    elif idx == 21: v = _distinct(r, 100000)
    elif idx <= 26: v = _distinct(r, r.randint(30000, 40000))
    elif idx == 27: v = sorted(_distinct(r, 100000))                 # 答案接近上限，远超 2^31
    elif idx == 28: v = list(range(0, N))                             # 含 0、连续整数
    elif idx == 29: v = sorted(_distinct(r, N), reverse=True)        # 答案 0
    elif idx == 30: v = [i * 2 for i in range(N)]                     # 大量“恰好 2 倍”的边界
    elif idx == 31:
        v = sorted(_distinct(r, 100000)); k = 50000
        v = v[:k][::-1] + v[k:]                                       # 前半逆序后半顺序
    elif idx == 32:
        v = sorted(_distinct(r, N))
        for _ in range(3000):
            a = r.randrange(N); b = min(N - 1, a + r.randint(1, 50)); v[a], v[b] = v[b], v[a]
    elif idx == 33: v = [0] + sorted(r.sample(range(1, VMAX + 1), N - 1))          # 最前面是速度 0
    elif idx == 34: v = _distinct(r, N, N * 3 // 2)
    elif idx == 35: v = [(i * 7919) % 100003 for i in range(1, N + 1)]
    else: v = _distinct(r, N)
    return f"{len(v)}\n" + "\n".join(map(str, v)) + "\n"

from pathlib import Path
import random, subprocess, sys, tempfile
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed), seed) for seed in range(1, 40)]
    assert len(set(cases)) == len(cases)
    for i, case in enumerate(cases):
        assert valid(case), i
        assert len(case) <= 1 << 20, i
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
