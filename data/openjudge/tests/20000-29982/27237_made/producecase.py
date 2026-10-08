import random, re, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "from collections import deque\n#import heapq\n\ndef bfs(s, e):\n    q = deque()\n    q.append((0, s, ''))\n    vis = set()\n    vis.add(s)\n    # q = []\n    #heapq.heappush(q, (0, s, ''))\n\n    while q:\n        step, pos, path = q.popleft()\n        #step, pos, path = heapq.heappop(q)\n        if pos == e:\n            return step, path\n\n        if pos * 3 not in vis:\n            q.append((step+1, pos*3, path+'H'))\n            vis.add(pos*3)\n            #heapq.heappush(q, (step+1, pos*3, path+'H'))\n        if int(pos // 2) not in vis:\n            vis.add(int(pos//2))\n            q.append((step+1, int(pos//2), path+'O'))\n            #heapq.heappush(q, (step+1, int(pos//2), path+'O'))\n\nwhile True:\n    n, m = map(int, input().split())\n    if n == 0 and m == 0:\n        break\n    step, path = bfs(n, m)\n    print(step)\n    print(path)\n"
SAMPLE_IN = '1 6\n0 0\n'
def _dist(s, e, cap=25):
    """BFS 最短跳跃次数，超过 cap 返回 None。"""
    from collections import deque
    q = deque([(s, 0)]); vis = {s}
    while q:
        p, d = q.popleft()
        if p == e:
            return d
        if d == cap:
            continue
        for x in (p * 3, p // 2):
            if x not in vis:
                vis.add(x); q.append((x, d + 1))
    return None


def valid(text):
    """题面：多组，每组两个正整数 n m (1<=n,m<=1000)，以 0 0 结束；数据保证有解且 k<=25。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) < 2 or lines[-1] != "0 0":
        return False
    for line in lines[:-1]:
        parts = line.split(" ")
        if len(parts) != 2 or not all(re.fullmatch(r"[1-9][0-9]*", x) for x in parts):
            return False
        n, m = map(int, parts)
        if not (1 <= n <= 1000 and 1 <= m <= 1000):
            return False
        if _dist(n, m) is None:
            return False
    return True


def _pair(r, lo_k, hi_k, fixed_n=None, fixed_m=None):
    while True:
        n = fixed_n if fixed_n is not None else r.randint(1, 1000)
        m = fixed_m if fixed_m is not None else r.randint(1, 1000)
        if n == m:
            continue
        d = _dist(n, m)
        if d is not None and lo_k <= d <= hi_k:
            return n, m


def generate_case(r, index):
    cases = []
    if index <= 8:
        # 小规模：起点小、步数少
        for _ in range(r.randint(1, 3)):
            while True:
                n, m = r.randint(1, 30), r.randint(1, 100)
                d = _dist(n, m, 12)
                if n != m and d is not None:
                    break
            cases.append((n, m))
    elif index <= 14:
        # 边界：n 或 m 取 1 / 1000
        picks = [(1, None), (None, 1), (1000, None), (None, 1000)]
        for _ in range(r.randint(3, 6)):
            fn, fm = r.choice(picks)
            cases.append(_pair(r, 1, 25, fn, fm))
        if index == 9:
            cases.append((1, 1000) if _dist(1, 1000) is not None else _pair(r, 1, 25, 1, None))
            cases.append((1000, 1))
    elif index <= 30:
        # 中大规模：随机 n m，步数 10..25
        for _ in range(r.randint(5, 15)):
            cases.append(_pair(r, 10, 25))
    else:
        # 深层：大量 k 在 22..25 的询问，卡掉不判重的搜索
        for _ in range(r.randint(15, 25)):
            cases.append(_pair(r, 22, 25))
    for n, m in cases:
        assert 1 <= n <= 1000 and 1 <= m <= 1000 and _dist(n, m) is not None
    return "\n".join(f"{a} {b}" for a, b in cases) + "\n0 0\n"


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(40):
            if index == 0: content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(27237 + index + attempt * 1000), index)
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content)
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
