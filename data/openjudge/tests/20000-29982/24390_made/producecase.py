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

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
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
