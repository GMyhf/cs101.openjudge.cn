import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def min_houses_to_buy(W, n, prices):\n    min_length = n + 1  # 初始化为最大长度+1，表示不可能的情况\n    current_sum = 0     # 当前窗口的价格总和\n    left = 0            # 窗口的左边界\n\n    # 遍历房屋价格数组\n    for right in range(n):\n        current_sum += prices[right]  # 扩展窗口的右边界\n\n        # 当当前总和大于等于W时，尝试缩小窗口的大小\n        while current_sum >= W and left <= right:\n            min_length = min(min_length, right - left + 1)\n            current_sum -= prices[left]  # 缩小窗口的左边界\n            left += 1\n\n    # 如果min_length没有更新，说明没有找到满足条件的窗口\n    return min_length if min_length <= n else 0\n\n# 读取输入\nW, n = map(int, input().split())\nprices = list(map(int, input().split()))\n\n# 计算结果并打印\nprint(min_houses_to_buy(W, n, prices))\n\n'
SAMPLE_IN = '7 6\n1 3 5 2 1 4\n'
SAMPLE_OUT = '2\n'
def generate_case(r):
    n = r.randint(2, 35); prices = [r.randint(1, 99999) for _ in range(n)]
    total = sum(prices)
    w = total + r.randint(1, 1000) if r.random() < .2 else r.randint(1, total)
    assert 0 < w < 10**9 and all(0 < x < 10**5 for x in prices)
    return f"{w} {n}\n" + " ".join(map(str, prices)) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(24678 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
