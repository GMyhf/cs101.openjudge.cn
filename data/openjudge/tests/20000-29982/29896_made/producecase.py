import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def solve():\n    import sys\n    input = sys.stdin.read\n    data = input().split()\n    \n    X = int(data[0])\n    N = int(data[1])\n    coins = list(map(int, data[2:2+N]))\n    \n    # 去除大于 X 的硬币（无用）\n    coins = [c for c in coins if c <= X]\n    if not coins:\n        if X == 0:\n            return 0\n        else:\n            return -1\n    \n    # 排序\n    coins.sort()\n    \n    # 必须要有 1，否则无法覆盖 1\n    if coins[0] > 1:\n        return -1\n    \n    max_reach = 0  # 当前能覆盖 [1, max_reach]\n    count = 0      # 使用的硬币数量\n    \n    while max_reach < X:\n        # 选择满足 coin <= max_reach + 1 的最大面值硬币\n        candidate = -1\n        for coin in coins:\n            if coin <= max_reach + 1:\n                candidate = coin\n            else:\n                break  # 因为已排序，后面的更大\n        \n        if candidate == -1:\n            return -1  # 无法扩展\n        \n        max_reach += candidate\n        count += 1\n        \n        if max_reach >= X:\n            break\n    \n    return count\n\n# 主程序\nprint(solve())\n'
SAMPLE_IN = '20 4\n1 2 5 10\n'
def generate_case(r):
    n = r.randint(2, 10); coins = sorted(r.sample(range(1, 40), n)); x = r.randint(1, 300)
    assert len(set(coins)) == n
    return f"{x} {n}\n" + " ".join(map(str, coins)) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(29896 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
