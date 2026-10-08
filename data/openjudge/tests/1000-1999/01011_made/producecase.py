import random,subprocess,sys,tempfile
from pathlib import Path
import re
def valid(text):
    """题面契约：若干两行块，首行木棍段数 n（1..64），次行 n 个 1..50 的正整数，最后一行 0。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    num = re.compile(r'(0|[1-9][0-9]*)$')
    i = 0
    while True:
        if i >= len(lines) or not num.match(lines[i]):
            return False
        n = int(lines[i]); i += 1
        if n == 0:
            return i == len(lines) and i > 1
        if n > 64 or i >= len(lines):
            return False
        toks = lines[i].split(' '); i += 1
        if len(toks) != n or not all(num.match(t) and 1 <= int(t) <= 50 for t in toks):
            return False
class _Budget(Exception):
    pass
def _ref_nodes(parts, budget):
    """按参考解的搜索顺序数 dfs 调用次数，超出 budget 抛 _Budget；用来确定性地挑出参考解跑得动的块。"""
    a = sorted(parts, reverse=True); N = len(a); tot = sum(a); cnt = [0]; used = []
    def dfs(unused, left, L):
        cnt[0] += 1
        if cnt[0] > budget:
            raise _Budget
        if unused == 0 and left == 0:
            return True
        if left == 0:
            left = L
        for i in range(N):
            if not used[i] and a[i] <= left:
                if i > 0 and not used[i - 1] and a[i] == a[i - 1]:
                    continue
                used[i] = True
                if dfs(unused - 1, left - a[i], L):
                    return True
                used[i] = False
                if a[i] == left or left == L:
                    break
        return False
    for L in range(a[0], tot // 2 + 1):
        if tot % L:
            continue
        used = [False] * N
        if dfs(N, 0, L):
            return cnt[0]
    return cnt[0]
def _cut(r, L, k, maxpart=50):
    parts = []
    for _ in range(k):
        rem = L
        while rem > 0:
            x = r.randint(1, min(maxpart, rem)); parts.append(x); rem -= x
    return parts
def _constructed(r, lo, hi):
    """把 k 根长 L 的原木随机切成 ≤50 的段，段数落在 [lo, hi]。"""
    while True:
        k = r.randint(1, 16); L = r.randint(2, 400)
        maxpart = r.choice([50, 50, 50, 30, 20, 10])
        p = _cut(r, L, k, maxpart)
        if lo <= len(p) <= hi:
            r.shuffle(p); return p
def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    fixed = {
        1: [[50], [1], [7, 7], [1, 2], [50, 49]],
        2: [[50] * 64, [1] * 64, [1] * 63 + [2], [50] * 63 + [1]],
        3: [[47] + [1] * 63, [2] * 62 + [3, 3], [25] * 64, [49, 1] * 32],
        5: [[13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 3, 5, 7, 11, 2], [50, 50, 50, 50, 49, 1], [26, 25, 25, 24]],
    }
    if seed in fixed:
        blocks = fixed[seed]
    else:
        blocks = []; total_nodes = 0
        want = r.randint(2, 8)
        lo, hi = (1, 20) if seed % 5 == 1 else (30, 64)
        need_hard = seed % 3 == 0          # 这些组至少放一块让参考解搜索 ≥2 万步的「难块」
        while len(blocks) < want:
            if seed == 4 or r.random() < 0.15:     # 纯随机段长：答案多半是总长本身
                p = [r.randint(1, 50) for _ in range(r.randint(lo, hi))]
            else:
                p = _constructed(r, lo, hi)
            try:
                c = _ref_nodes(p, 400_000)
            except _Budget:
                continue
            if total_nodes + c > 1_000_000:
                continue
            if need_hard and len(blocks) == want - 1 and c < 20_000:
                continue
            need_hard = need_hard and c < 20_000
            total_nodes += c; blocks.append(p)
    return ''.join(f"{len(p)}\n{' '.join(map(str, p))}\n" for p in blocks) + '0\n'
REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1011: Sticks\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/pctbook/01011/\n# License: not declared in source collection; no license is inferred.\nimport sys\ndef dfs(unused, left, len):\n    if unused == 0 and left == 0:\n        return True\n    if left == 0:\n        left = len\n\n    for i in range(N):\n        if used[i] == False and length[i] <= left:\n            if i > 0:\n                if used[i - 1] == False and length[i] == length[i - 1]:\n                    continue  # 不要在同一个位置多次尝试相同长度的木棒，剪枝1\n\n            used[i] = True\n            if dfs(unused - 1, left - length[i], len):\n                return True\n            used[i] = False\n\n            # 不能仅仅通过替换最后一根木棒来达到目的，剪枝3\n            # 替换第一个根棍子是没有用的，因为就算现在不用，也总会用到这根木棍，剪枝2\n\n            # 如果我们进行尝试的时候，所使用的这根木棍长度恰好与为达到给定长度所需要的长度相等\n            # （也就是说使用了这根木棍就可以开始新尝试），\n            # 亦或此时恰好开始一次新的尝试，得到的结果是False，那么就说明这个给定长度不满足条件。\n            if length[i] == left or left == len:\n                break\n\n    return False\n\n\nwhile True:\n    N = int(input())\n    if N == 0:\n        break\n\n    length = [int(x) for x in input().split()]\n    length.sort(reverse=True)  # 排序是为了从长到短拿木棒进行尝试\n\n    totalLen = sum(length)\n\n    for L in range(length[0], totalLen//2 + 1):\n        if totalLen % L:\n            continue  # 不是木棒长度和的因子的长度，直接否定\n\n        used = [False] * 65\n        if dfs(N, 0, L):\n            print(L)\n            break\n    else:\n        print(totalLen)\n'
NUMBER=1011
SAMPLE='9\n5 2 1 5 2 1 5 2 1\n4\n1 2 3 4\n0\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'m.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[generate(NUMBER,s) for s in range(1, 40)]):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
