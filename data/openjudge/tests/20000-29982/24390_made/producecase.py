import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'from collections import deque\n\n\ndef solve():\n    N = int(input().strip())\n    s = input().strip()\n\n    # 初始状态转成整数（二进制掩码）\n    start = int(s, 2)\n    #print(f"start = {start}")\n    target1 = 0  # 全 0\n    target2 = (1 << N) - 1  # 全 1\n\n    # 预先计算每个位置的翻转掩码\n    masks = []\n    for i in range(N):\n        mask = 1 << i\n        if i > 0:\n            mask |= 1 << (i - 1)\n        if i < N - 1:\n            mask |= 1 << (i + 1)\n        masks.append(mask)\n\n    # BFS\n    q = deque([(start, 0)])\n    visited = {start}\n\n    while q:\n        state, step = q.popleft()\n        if state == target1 or state == target2:\n            print(step)\n            return\n        for mask in masks:\n            nxt = state ^ mask  # 翻转操作，就是「0→1，1→0」，等价于 XOR 1\n            if nxt not in visited:\n                visited.add(nxt)\n                q.append((nxt, step + 1))\n\n\nif __name__ == "__main__":\n    solve()\n\n'
SAMPLE_IN = '5\n01101\n'
def generate_case(r):
    n = r.randint(2, 12); bits = [0] * n
    steps = r.randint(1, 12)
    for _ in range(steps):
        i = r.randrange(n)
        for j in (i - 1, i, i + 1):
            if 0 <= j < n: bits[j] ^= 1
    assert all(x in (0, 1) for x in bits)
    return f"{n}\n" + "".join(map(str, bits)) + "\n"

def min_ops(s):
    # 独立 oracle：枚举目标颜色与第 1 个位置是否施法，其余位置被唯一确定；无解返回 None
    n = len(s); b = list(map(int, s)); best = None
    for t in (0, 1):
        for p0 in (0, 1):
            c = b[:]; cnt = 0
            for i in range(n):
                press = p0 if i == 0 else int(c[i - 1] != t)
                if press:
                    cnt += 1
                    for j in (i - 1, i, i + 1):
                        if 0 <= j < n: c[j] ^= 1
            if c[n - 1] == t and (best is None or cnt < best): best = cnt
    return best

def valid(text):
    # 题面：第一行 N（1<=N<=20），第二行长度为 N 的 01 串；保证可以做到颜色一致
    if not text.endswith("\n"): return False
    lines = text[:-1].split("\n")
    if len(lines) != 2 or not lines[0].isdigit() or lines[0] != str(int(lines[0])): return False
    n = int(lines[0])
    if not 1 <= n <= 20 or len(lines[1]) != n or set(lines[1]) - set("01"): return False
    return min_ops(lines[1]) is not None

def extra_cases():
    # 补充：N=1、N=20/19 的最远状态、满规模随机可解状态（含只能变成全 1 的）
    out = ["1\n0\n", "1\n1\n", "20\n" + "0" * 20 + "\n",
           "20\n10111111111100111110\n", "19\n1011111111111100001\n", "20\n" + "1" * 20 + "\n"]
    r = random.Random(243900)
    while len(out) < 30:
        n = r.choice([20, 20, 20, 19, 18, r.randint(13, 20)])
        s = "".join(r.choice("01") for _ in range(n))
        c = f"{n}\n{s}\n"
        if min_ops(s) is not None and c not in out: out.append(c)
    return out

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(40):
            if index == 0: content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(24390 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
        for content in extra_cases():
            assert content not in seen
            seen.append(content); index += 1
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=20, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
