import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "def kadane(nums):\n    max_ending_here = max_so_far = nums[0]\n    for x in nums[1:]:\n        max_ending_here = max(x, max_ending_here + x)\n        max_so_far = max(max_so_far, max_ending_here)\n    return max_so_far\n\ndef max_sum_shopping(values):\n    # 不放回商品的情况下的最大价值总和\n    max_without_deletion = kadane(values)\n\n    # 如果整个数列的和都是负的，则土豪只能选择一个价值最大的商品\n    if max_without_deletion < 0:\n        return max(values)\n\n    # 准备两个数组来存储从左到右和从右到左的最大子数组和\n    left_max_sums = [0] * len(values)\n    right_max_sums = [0] * len(values)\n\n    # 从左到右的最大子数组和\n    current = 0\n    for i in range(len(values)):\n        current = max(0, current + values[i])\n        left_max_sums[i] = current\n\n    # 从右到左的最大子数组和\n    current = 0\n    for i in range(len(values) - 1, -1, -1):\n        current = max(0, current + values[i])\n        right_max_sums[i] = current\n\n    # 放回一个商品时的最大价值总和\n    max_with_deletion = 0\n    for i in range(1, len(values) - 1):\n        max_with_deletion = max(max_with_deletion, left_max_sums[i - 1] + right_max_sums[i + 1])\n\n    # 返回放回一个商品和不放回一个商品两种情况下的最大价值\n    return max(max_with_deletion, max_without_deletion)\n\n# 读取输入并处理\nvalues_str = input().strip()\nvalues = list(map(int, values_str.split(',')))\nprint(max_sum_shopping(values))\n"
SAMPLE_IN = '1,-5,0,3\n'
SAMPLE_OUT = '4\n'
def generate_case(r): return ",".join(str(r.randint(-30, 40)) for _ in range(r.randint(2, 30))) + "\n"

assert SAMPLE_IN == '1,-5,0,3\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(20744 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
