import random, re, subprocess, tempfile
from pathlib import Path

# 参考解：按时间排序后逐个时刻推进；S 内最小票数用“票数频次桶 + 单调指针”维护，S 外最大票数单调不减，O(N + K)。
# （旧版内嵌的是多题合并脚本，每个时刻都对全部候选人排序，N 上万就跑不动，只能配 n<=20 的小数据。）
REFERENCE_SOURCE = r'''import sys
def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    rec = sorted((int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(n))
    s = data[2 + 2 * n:2 + 2 * n + k]
    in_s = [False] * 314160
    for x in s:
        in_s[int(x)] = True
    cnt = [0] * 314160
    freq = [0] * (n + 2)          # freq[c]：S 中恰有 c 票的人数
    freq[0] = k
    min_s = 0                     # S 中最少票数（只增不减）
    max_other = 0                 # S 外最多票数（只增不减）；K <= 314158，S 外至少一人
    ans = 0
    last = 0
    i = 0
    while i < n:
        t = rec[i][0]
        if min_s > max_other:
            ans += t - last
        while i < n and rec[i][0] == t:
            c = rec[i][1]
            if in_s[c]:
                freq[cnt[c]] -= 1
                cnt[c] += 1
                freq[cnt[c]] += 1
                while freq[min_s] == 0:
                    min_s += 1
            else:
                cnt[c] += 1
                if cnt[c] > max_other:
                    max_other = cnt[c]
            i += 1
        last = t
    print(ans)
main()
'''
SAMPLE_IN = '10 2  \n3 1 4 1 5 1 4 3 6 5 8 3 7 5 8 5 9 1 10 5  \n1 5\n'
SAMPLE_OUT = '3\n'
MAXC = 314159
LINE_RE = re.compile(r" *[0-9]+( +[0-9]+)* *")


def valid(text):
    """题面：第一行 N K；第二行 2N 个整数 T1 C1 ... TN CN；第三行 K 个整数 S1..SK（候选人集合，互异）。
    1<=N<=314159，1<=K<=314158，1<=Ti<=1000000，1<=Ci,Si<=314159。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 3 or not all(LINE_RE.fullmatch(l) for l in lines):
        return False
    head = lines[0].split()
    if len(head) != 2:
        return False
    n, k = map(int, head)
    if not (1 <= n <= 314159 and 1 <= k <= 314158):
        return False
    rec = list(map(int, lines[1].split()))
    s = list(map(int, lines[2].split()))
    if len(rec) != 2 * n or len(s) != k:
        return False
    if not all(1 <= t <= 1000000 for t in rec[0::2]):
        return False
    if not all(1 <= c <= MAXC for c in rec[1::2]):
        return False
    if not all(1 <= x <= MAXC for x in s) or len(set(s)) != k:
        return False
    return True


def fmt(rec, s, r, order="shuffle"):
    rec = list(rec)
    if order == "shuffle":
        r.shuffle(rec)
    elif order == "sorted":
        rec.sort()
    elif order == "nearly":            # 大体有序，局部打乱
        rec.sort()
        for _ in range(len(rec) // 10):
            i = r.randrange(len(rec)); j = min(len(rec) - 1, i + r.randint(1, 5))
            rec[i], rec[j] = rec[j], rec[i]
    s = list(s); r.shuffle(s)
    return f"{len(rec)} {len(s)}\n" + " ".join(f"{t} {c}" for t, c in rec) + "\n" + " ".join(map(str, s)) + "\n"


def votes(r, n, s_ids, other_ids, bias, tmax, dup=0.0):
    """S 里的人每票权重 bias，其余人权重 1；时间戳 1..tmax 随机（dup 概率复用上一个时间戳，制造同刻多票）。"""
    pool = list(s_ids) + list(other_ids)
    w = [bias] * len(s_ids) + [1.0] * len(other_ids)
    cs = r.choices(pool, weights=w, k=n)
    ts = []
    for _ in range(n):
        if ts and r.random() < dup:
            ts.append(r.choice(ts[-5:]))
        else:
            ts.append(r.randint(1, tmax))
    return list(zip(ts, cs))


def pick_ids(r, m):
    return r.sample(range(1, MAXC + 1), m)


def g_small(r):
    n = r.randint(1, 30)
    p = r.randint(1, 7)
    ids = pick_ids(r, p + 2)
    k = r.randint(1, min(p + 1, 6))
    s, others = ids[:k], ids[k:]
    rec = votes(r, n, s, others[:max(1, p - k)], r.choice([1, 1.5, 2, 3]), r.choice([n, 2 * n + 3, 15]), dup=r.choice([0, .3]))
    return fmt(rec, s, r, r.choice(["shuffle", "sorted", "nearly"]))


def g_tie(r):
    # 两个候选人轮流得票，大量时刻 S 与 S 外票数相等：卡“>=”代替严格“>”
    n = r.randint(10, 40)
    a, b, c = pick_ids(r, 3)
    rec = []
    t = 0
    for i in range(n):
        t += r.randint(1, 4)
        rec.append((t, a if i % 2 == 0 else (b if r.random() < .8 else c)))
    return fmt(rec, [a] if r.random() < .5 else [b], r)


def g_big(r, kind):
    if kind == "few":            # 少量候选人，S 和 S 外反复交替领先
        n = 60000; ids = pick_ids(r, 6); s = ids[:2]
        rec = votes(r, n, s, ids[2:], 1.05, 1000000, dup=.2)
    elif kind == "many":         # 候选人很多，卡“每个时刻排序/扫一遍全体候选人”
        n = 60000; ids = pick_ids(r, 30000); s = ids[:30]
        rec = votes(r, n, s, ids[30:], 400, 1000000, dup=.05)
    elif kind == "k1":
        n = 60000; ids = pick_ids(r, 3000); s = ids[:1]
        rec = votes(r, n, s, ids[1:], 60, 1000000, dup=.1)
    elif kind == "bigk":         # K 很大：S 中每人都得票后才可能满足
        # S 中每人两票（多在前半段），S 外 3000 人各一票，另有一人后段拿到两票把局面打破
        k = 22000; ids = pick_ids(r, k + 3001); s = ids[:k]
        rec = [(r.randint(1, 600000), x) for x in s for _ in range(2)]
        rec += [(r.randint(1, 1000000), x) for x in ids[k:k + 3000]]
        rec += [(r.randint(700000, 800000), ids[-1]), (r.randint(800000, 950000), ids[-1])]
    elif kind == "sorted-distinct":   # 时间戳 1..1e6 递增，答案接近 1e6 量级
        n = 60000; ids = pick_ids(r, 50); s = ids[:3]
        ts = sorted(r.sample(range(1, 1000001), n - 1) + [1000000])
        cs = r.choices(ids, weights=[30] * 3 + [1] * 47, k=n)
        cs[0] = s[0]; cs[1] = s[1]; cs[2] = s[2]
        rec = list(zip(ts, cs))
    elif kind == "same-time":         # 所有票同一时刻投出，答案 0
        n = 60000; ids = pick_ids(r, 100); s = ids[:5]
        t = r.randint(1, 1000000)
        rec = [(t, c) for _, c in votes(r, n, s, ids[5:], 5, 1)]
    elif kind == "ghost":             # S 中有人从未得票，答案 0
        n = 60000; ids = pick_ids(r, 200); s = ids[:10]
        rec = votes(r, n, s[:-1], ids[10:], 50, 1000000)
    else:
        raise ValueError(kind)
    return fmt(rec, s, r, r.choice(["shuffle", "nearly"]))


FIXED = [
    "1 1\n5 7\n7\n",                      # N=1：唯一一票之后时间就结束了
    "2 1\n1 3 2 3\n3\n",
    "2 1\n2 9 1 314159\n314159\n",         # 输入乱序、编号上限
    "3 1\n1 1 1 2 5 1\n1\n",              # 同一时刻两票打平
    "3 2\n4 1 2 2 9 3\n1 2\n",
    "2 5\n1 1 2 2\n1 2 3 4 5\n",           # K > N，答案 0
    "4 1\n1000000 1 1 2 1 2 500000 1\n2\n",
]


def build_cases():
    cases = [SAMPLE_IN] + FIXED
    plan = ["small"] * 14 + ["tie"] * 3 + ["mid"] * 7 + ["few", "few", "many", "k1", "bigk", "sorted-distinct", "same-time", "ghost"]
    seed = 0
    for kind in plan:
        while True:
            seed += 1
            r = random.Random(27384 * 1000 + seed)
            if kind == "small":
                c = g_small(r)
            elif kind == "tie":
                c = g_tie(r)
            elif kind == "mid":
                n = r.randint(1000, 5000); p = r.randint(5, 600); ids = pick_ids(r, p); k = r.randint(1, max(1, p // 10))
                c = fmt(votes(r, n, ids[:k], ids[k:], r.choice([2, 5, 20]), r.choice([n, 1000000]), dup=.2), ids[:k], r)
            else:
                c = g_big(r, kind)
            if c not in cases:
                break
        cases.append(c)
    return cases


def main():
    root = Path(__file__).parent / "data"
    with tempfile.NamedTemporaryFile("w", suffix=".py") as h:
        h.write(REFERENCE_SOURCE); h.flush()
        for i, c in enumerate(build_cases()):
            assert valid(c), i
            p = subprocess.run(["python3", h.name], input=c, text=True, capture_output=True, check=True)
            if i == 0:
                assert p.stdout == SAMPLE_OUT
            (root / f"{i}.in").write_text(c); (root / f"{i}.out").write_text(p.stdout)


if __name__ == "__main__":
    main()
