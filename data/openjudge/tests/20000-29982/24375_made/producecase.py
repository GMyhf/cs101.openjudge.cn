import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '#蒋子轩\ndef dfs(rem_sticks,rem_len,target):\n    if rem_sticks==0 and rem_len==0:\n        return True\n    if rem_len==0:\n        rem_len=target\n    for i in range(n):\n        if not used[i] and lens[i]<=rem_len:\n            used[i]=True\n            if dfs(rem_sticks-1,rem_len-lens[i],target):\n                return True\n            else:\n                used[i]=False\n                if lens[i]==rem_len or rem_len==target:\n                    return False\n    return False\nwhile True:\n    n=int(input())\n    if n==0:\n        break\n    lens=list(map(int,input().split()))\n    lens.sort(reverse=True)\n    total_len=sum(lens)\n    for l in range(lens[0],total_len//2+1):\n        if total_len%l!=0:\n            continue\n        used=[False]*n\n        if dfs(n,l,l):\n            print(l)\n            break\n    else:\n        print(total_len)\n'
SAMPLE_IN = '9\n5 2 1 5 2 1 5 2 1\n4\n1 2 3 4\n0\n'
SAMPLE_OUT = '6\n5\n'
def generate_case(r):
    cases = []
    for _ in range(r.randint(2, 4)):
        target = r.randint(3, 18)
        pieces = []
        for _ in range(r.randint(2, 5)):
            remaining = target
            group = []
            while remaining > 0:
                part = r.randint(1, remaining)
                group.append(part); remaining -= part
            pieces.extend(group)
        r.shuffle(pieces)
        assert sum(pieces) % target == 0 and len(pieces) <= 64
        cases.extend([str(len(pieces)), " ".join(map(str, pieces))])
    return "\n".join(cases + ["0"]) + "\n"


def valid(text):
    # 题面：多个实例，每个实例两行：n（1..64），n 个空格分隔的正整数（每段 1..50）；最后一行 0 结束
    if not text.endswith("\n"): return False
    lines = text[:-1].split("\n")
    if lines[-1] != "0" or len(lines) % 2 != 1 or len(lines) < 3: return False
    for k in range(0, len(lines) - 1, 2):
        a = lines[k]
        if not a.isdigit() or a != str(int(a)) or not 1 <= int(a) <= 64: return False
        toks = lines[k + 1].split(" ")
        if len(toks) != int(a): return False
        for t in toks:
            if not t.isdigit() or t != str(int(t)) or not 1 <= int(t) <= 50: return False
    return True

def solve_one(a):
    # 独立 oracle：降序 + 跳过同长度 + 首段失败即剪枝
    a = sorted(a, reverse=True); n = len(a); tot = sum(a)
    for L in range(a[0], tot + 1):
        if tot % L: continue
        used = [False] * n
        def dfs(start, cur, left):
            if left == 0: return True
            if cur == L: return dfs(0, 0, left - 1)
            prev = -1
            for i in range(start, n):
                if used[i] or a[i] == prev or cur + a[i] > L: continue
                used[i] = True
                if dfs(i + 1, cur + a[i], left): return True
                used[i] = False; prev = a[i]
                if cur == 0 or cur + a[i] == L: return False
            return False
        if dfs(0, 0, tot // L): return L

def oracle(text):
    lines = text.split("\n"); out = []
    for k in range(0, len(lines) - 2, 2):
        out.append(str(solve_one(list(map(int, lines[k + 1].split())))))
    return "\n".join(out) + "\n"

REF_BUDGET = 300000

def ref_within_budget(text, budget=REF_BUDGET):
    # 与 REFERENCE_SOURCE 同一算法的计数版，统计 dfs 调用次数
    import sys
    sys.setrecursionlimit(10000)
    lines = text.split("\n"); calls = [0]
    for k in range(0, len(lines) - 2, 2):
        lens = sorted(map(int, lines[k + 1].split()), reverse=True); n = len(lens)
        used = [False] * n
        def dfs(rem_sticks, rem_len, target):
            calls[0] += 1
            if calls[0] > budget: raise OverflowError
            if rem_sticks == 0 and rem_len == 0: return True
            if rem_len == 0: rem_len = target
            for i in range(n):
                if not used[i] and lens[i] <= rem_len:
                    used[i] = True
                    if dfs(rem_sticks - 1, rem_len - lens[i], target): return True
                    used[i] = False
                    if lens[i] == rem_len or rem_len == target: return False
            return False
        tot = sum(lens)
        try:
            for l in range(lens[0], tot // 2 + 1):
                if tot % l: continue
                used[:] = [False] * n
                if dfs(n, l, l): break
        except OverflowError:
            return False
    return True

def cut_instance(r, L, sticks, maxn=64):
    # 把 sticks 根长 L 的木棍随机切成每段 <=50，总段数 <=64
    while True:
        pieces = []
        for _ in range(sticks):
            rem = L
            while rem > 0:
                hi = min(50, rem); part = r.randint(1, hi) if r.random() < .7 else r.randint((hi + 1) // 2, hi)
                pieces.append(part); rem -= part
        if len(pieces) <= maxn:
            r.shuffle(pieces); return pieces
        sticks = max(2, sticks - 1)  # 段数超了就少切一根，避免长时间拒绝采样

def fmt(insts):
    return "\n".join(f"{len(p)}\n{' '.join(map(str, p))}" for p in insts) + "\n0\n"

FIXED = [
    fmt([[7]]),                       # n=1
    fmt([[50]]),                      # n=1，最长段
    fmt([[3, 4]]),                    # 总长为质数，答案=总长
    fmt([[50] * 64]),                 # n=64，全为 50
    fmt([[1] * 64]),                  # n=64，全为 1
    fmt([[49, 1] * 32]),              # 答案 50
    fmt([[13, 17, 19, 23, 29, 31, 37, 41, 43, 47]]),
]

def gen_big(r):
    insts = []
    for _ in range(r.randint(1, 3)):
        L = r.choice([r.randint(30, 60), r.randint(50, 120), r.randint(60, 250)])
        sticks = r.randint(2, max(2, min(20, 64 * 25 // L)))
        insts.append(cut_instance(r, L, sticks))
    return fmt(insts)

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        cases = []
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(24375 + index + attempt * 1000))
                    if content not in cases: break
                else: raise AssertionError("insufficient diversity")
            cases.append(content)
        cases += [c for c in FIXED if c not in cases]
        seed = 0
        while len(cases) < 40:
            c = gen_big(random.Random(243750 + seed)); seed += 1
            if c in cases: continue
            # 题面说数据已弱化：参考解（弱剪枝）递归调用超过 REF_BUDGET 次的输入不收（按步数而非计时，保证可复现）
            if not ref_within_budget(c): continue
            cases.append(c)
        for index, content in enumerate(cases):
            assert valid(content), index
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            assert result.stdout == oracle(content), index
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
