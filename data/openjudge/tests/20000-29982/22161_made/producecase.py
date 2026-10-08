import random, subprocess, tempfile
from pathlib import Path
# 原 REFERENCE_SOURCE（公开题解）在权值相同的内部节点比较时 None < None 抛 TypeError，且未按「字符集最小字符」比较；
# 原数据权值全取 2 的幂避开了平局，也从未出现 01 串。现换成按题面规则实现的参考解。
REFERENCE_SOURCE = '# 修正版参考解：按题面规则比较节点——先比权值，权值相同比「字符集里最小字符」，小者作左子。\nimport heapq\nimport sys\n\ndef main():\n    lines = sys.stdin.read().split("\\n")\n    n = int(lines[0])\n    heap = []\n    for i in range(1, n + 1):\n        c, w = lines[i].split()\n        heapq.heappush(heap, (int(w), c, c))          # (权值, 最小字符, 子树)\n    while len(heap) > 1:\n        w1, m1, t1 = heapq.heappop(heap)\n        w2, m2, t2 = heapq.heappop(heap)\n        heapq.heappush(heap, (w1 + w2, min(m1, m2), (t1, t2)))\n    root = heap[0][2]\n    codes = {}\n    def walk(t, path):\n        if isinstance(t, str):\n            codes[t] = path\n        else:\n            walk(t[0], path + "0"); walk(t[1], path + "1")\n    walk(root, "")\n    out = []\n    for line in lines[n + 1:]:\n        s = line.strip()\n        if not s:\n            continue\n        if s[0] in "01":\n            res, t = [], root\n            for b in s:\n                t = t[0] if b == "0" else t[1]\n                if isinstance(t, str):\n                    res.append(t); t = root\n            out.append("".join(res))\n        else:\n            out.append("".join(codes[c] for c in s))\n    print("\\n".join(out))\n\nmain()\n'
SAMPLE_IN = '3\ng 4\nd 8\nc 10\ndc\n110\n'
SAMPLE_OUT = '110\ndc\n'
def generate_case(r):
    chars = r.sample("abcdefghi", r.randint(3, 6)); lines = [str(len(chars))]
    weights = [2 ** (i * 4) for i in range(len(chars))]
    assert len(set(chars)) == len(chars) and len(set(weights)) == len(weights)
    for c, weight in zip(chars, weights): lines.append(f"{c} {weight}")
    words = ["".join(r.choice(chars) for _ in range(r.randint(1, 8))) for _ in range(3)]
    return "\n".join(lines + words) + "\n"

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def build_tree(pairs):
    import heapq
    heap = [(w, c, c) for c, w in pairs]; heapq.heapify(heap)
    while len(heap) > 1:
        w1, m1, t1 = heapq.heappop(heap); w2, m2, t2 = heapq.heappop(heap)
        heapq.heappush(heap, (w1 + w2, min(m1, m2), (t1, t2)))
    return heap[0][2]

def valid(text):
    """题面：首行整数 n；随后 n 行「字符 权值」，字符为英文字母（互异）；其后若干行，每行是字符集里字母组成的串或 01 编码串（须能完整解码）。"""
    try:
        if not text.endswith("\n"): return False
        lines = text[:-1].split("\n")
        if not lines[0].isdigit(): return False
        n = int(lines[0])
        if n < 1 or len(lines) < n + 2: return False
        pairs = []
        for line in lines[1:n + 1]:
            t = line.split(" ")
            if len(t) != 2 or len(t[0]) != 1 or t[0] not in LETTERS or not t[1].isdigit(): return False
            pairs.append((t[0], int(t[1])))
        chars = {c for c, _ in pairs}
        if len(chars) != n: return False
        root = build_tree(pairs) if n >= 2 else None
        for q in lines[n + 1:]:
            if not q: return False
            if set(q) <= set("01"):
                if root is None: return False
                t = root
                for b in q:
                    t = t[int(b)]
                    if isinstance(t, str): t = root
                if t is not root: return False
            elif not set(q) <= chars: return False
        return True
    except Exception:
        return False

def extra_cases():
    """补充：大量同权值（叶-叶、叶-内部、内部-内部平局）、01 串解码、n=2 与 n=26 边界（追加在原 20 组之后）。"""
    r = random.Random(221610); out = []
    lower = "abcdefghijklmnopqrstuvwxyz"
    def make(pairs, nq, maxlen):
        root = build_tree(pairs); codes = {}
        def walk(t, path):
            if isinstance(t, str): codes[t] = path
            else: walk(t[0], path + "0"); walk(t[1], path + "1")
        walk(root, "")
        chars = [c for c, _ in pairs]; qs = []
        for i in range(nq):
            w = "".join(r.choice(chars) for _ in range(r.randint(1, maxlen)))
            qs.append("".join(codes[c] for c in w) if i % 2 else w)
        r.shuffle(qs)
        return "\n".join([str(len(pairs))] + [f"{c} {w}" for c, w in pairs] + qs) + "\n"
    out.append(make([("b", 5), ("a", 5)], 4, 6))                       # n=2，同权值
    out.append(make([(c, 1) for c in r.sample(lower, 26)], 8, 30))      # 26 个全等权值
    out.append(make([(c, 7) for c in r.sample(lower, 5)], 6, 10))
    fib = [1, 1]
    while len(fib) < 20: fib.append(fib[-1] + fib[-2])
    cs = r.sample(lower, 20)
    out.append(make(list(zip(cs, fib)), 8, 20))                         # 斐波那契权值：叶与内部节点平局、深树
    out.append(make([("x", 2), ("y", 1), ("z", 1), ("a", 4), ("q", 8)], 6, 12))  # 合并出的 ({y,z},2) 与 x 平局
    for k in range(15):
        n = r.choice([3, 4, 6, 10, 16, 26, r.randint(2, 26)])
        hi = r.choice([1, 2, 3, 5, 10, 100])
        out.append(make([(c, r.randint(1, hi)) for c in r.sample(lower, n)], r.randint(4, 12), r.choice([5, 20, 60])))
    return out

def main():
    assert SAMPLE_IN == '3\ng 4\nd 8\nc 10\ndc\n110\n'
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(22161 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError('insufficient diversity')
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
        for index, content in enumerate(extra_cases(), start=20):
            assert valid(content) and content not in seen
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=30, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
    assert all(valid(c) for c in seen)

if __name__ == "__main__":
    main()
