import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import gc\nimport heapq\nimport sys\n\n\ndef solve():\n    # 暂时禁用垃圾回收以提升执行速度\n    gc.disable()\n\n    # 以字节流形式读取输入，速度最快\n    input_bytes = sys.stdin.buffer.read().split()\n    if not input_bytes:\n        return\n\n    # 快速转换为整型列表\n    data = list(map(int, input_bytes))\n    N = data[0]\n    K = data[1]\n\n    # 利用高速 C 切片分离 A 轮和 B 轮数据\n    As = data[2::2]\n    Bs = data[3::2]\n\n    # 第一轮筛选：找出 As 中值最大的前 K 个索引\n    # 使用内置的 As.__getitem__ 替代 lambda 表达式，速度极快\n    if K < 1000:\n        top_k = heapq.nlargest(K, range(N), key=As.__getitem__)\n    else:\n        top_k = sorted(range(N), key=As.__getitem__, reverse=True)[:K]\n\n    # 第二轮筛选：在 top_k 索引中，找出使 Bs 值最大的索引\n    winner_idx = max(top_k, key=Bs.__getitem__)\n\n    # 输出 1 基准的牛编号\n    print(winner_idx + 1)\n\n\nif __name__ == "__main__":\n    solve()\n'
SAMPLE_IN = '5 3\n3 10\n9 2\n5 6\n8 4\n6 5\n'
def generate_case(r):
    n = r.randint(2, 80); k = r.randint(1, n); avals = r.sample(range(1, 10**9), n); bvals = r.sample(range(1, 10**9), n)
    assert len(set(avals)) == n and len(set(bvals)) == n
    return f"{n} {k}\n" + "\n".join(f"{a} {b}" for a, b in zip(avals, bvals)) + "\n"

def valid(text):
    """题面契约：首行 N K（1<=N<=1e6, 1<=K<=N），随后恰 N 行 Ai Bi（1..1e9）；
    第一轮 Ai 互不相同，第二轮（前 K 名）Bi 互不相同。"""
    if not text.endswith("\n"): return False
    lines = text[:-1].split("\n")
    def ints(line, cnt):
        parts = line.split(" ")
        if len(parts) != cnt or not all(x.isdigit() and (x == "0" or x[0] != "0") for x in parts): return None
        return list(map(int, parts))
    first = ints(lines[0], 2)
    if not first: return False
    n, k = first
    if not (1 <= n <= 10**6 and 1 <= k <= n) or len(lines) != n + 1: return False
    rows = []
    for line in lines[1:]:
        ab = ints(line, 2)
        if not ab or not all(1 <= v <= 10**9 for v in ab): return False
        rows.append(ab)
    if len({a for a, _ in rows}) != n: return False
    top = sorted(rows, key=lambda x: -x[0])[:k]
    return len({b for _, b in top}) == k

def special_case(index):
    """补充规模与边界：最小规模、K=1、K=N、全局最大 B 被第一轮淘汰、满值 1e9、大 N（受单组 1MB 限制取 4.5 万/7 万）。"""
    r = random.Random(310410 + index)
    def pack(n, k, a, b):
        return f"{n} {k}\n" + "\n".join(f"{x} {y}" for x, y in zip(a, b)) + "\n"
    if index == 30:
        return "1 1\n1000000000 1000000000\n"
    if index == 31:
        return "2 1\n2 1\n1 1000000000\n"
    if index in (32, 33, 34, 36, 37, 39):
        n = 45000
        a = r.sample(range(1, 10**9 + 1), n); b = r.sample(range(1, 10**9 + 1), n)
        if index == 32: k = n
        elif index == 33: k = 1
        elif index == 36: k = n - 1
        elif index == 39: k = 999
        else: k = r.randint(n // 4, 3 * n // 4)
        if index in (34, 36):
            # 让全局 B 最大的牛恰好排在第一轮第 k+1 名而被淘汰
            order = sorted(range(n), key=lambda i: -a[i])
            out = order[k]; best = max(range(n), key=lambda i: b[i])
            b[out], b[best] = b[best], b[out]
        if index == 37:
            a.sort()
        return pack(n, k, a, b)
    if index == 35:
        n = 70000; a = list(range(1, n + 1)); b = list(range(1, n + 1)); r.shuffle(a); r.shuffle(b)
        return pack(n, n // 2, a, b)
    if index == 38:
        n = 1000; a = r.sample(range(1, 10**9 + 1), n); b = r.sample(range(1, 10**9 + 1), n)
        return pack(n, 1000, a, b)
    raise ValueError(index)

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(40):
            if index == 0: content = SAMPLE_IN
            elif index >= 30: content = special_case(index)
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(31041 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
