import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "def kadane(nums):\n    max_ending_here = max_so_far = nums[0]\n    for x in nums[1:]:\n        max_ending_here = max(x, max_ending_here + x)\n        max_so_far = max(max_so_far, max_ending_here)\n    return max_so_far\n\ndef max_sum_shopping(values):\n    # 不放回商品的情况下的最大价值总和\n    max_without_deletion = kadane(values)\n\n    # 如果整个数列的和都是负的，则土豪只能选择一个价值最大的商品\n    if max_without_deletion < 0:\n        return max(values)\n\n    # 准备两个数组来存储从左到右和从右到左的最大子数组和\n    left_max_sums = [0] * len(values)\n    right_max_sums = [0] * len(values)\n\n    # 从左到右的最大子数组和\n    current = 0\n    for i in range(len(values)):\n        current = max(0, current + values[i])\n        left_max_sums[i] = current\n\n    # 从右到左的最大子数组和\n    current = 0\n    for i in range(len(values) - 1, -1, -1):\n        current = max(0, current + values[i])\n        right_max_sums[i] = current\n\n    # 放回一个商品时的最大价值总和\n    max_with_deletion = 0\n    for i in range(1, len(values) - 1):\n        max_with_deletion = max(max_with_deletion, left_max_sums[i - 1] + right_max_sums[i + 1])\n\n    # 返回放回一个商品和不放回一个商品两种情况下的最大价值\n    return max(max_with_deletion, max_without_deletion)\n\n# 读取输入并处理\nvalues_str = input().strip()\nvalues = list(map(int, values_str.split(',')))\nprint(max_sum_shopping(values))\n"
SAMPLE_IN = '1,-5,0,3\n'
SAMPLE_OUT = '4\n'
def generate_case(r):
    values = [r.randint(-30, 40) for _ in range(r.randint(2, 30))]
    assert values
    return ",".join(map(str, values)) + "\n"

def valid(text):
    """题面：一行，逗号分隔的整数（商品价值，可能为负）。题面未给个数与取值上限；至少一个数。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    parts = text[:-1].split(",")
    try:
        vals = [int(x) for x in parts]
    except ValueError:
        return False
    return all(x == str(v) for x, v in zip(parts, vals)) and len(vals) >= 1


def extra_cases():
    """补充：原 20 组 n<=30，O(n^2)/O(n^3) 暴力都能过，也没有 n=1、全负、全零、全正、
    必须放回中间大负数等分支。题面没给规模，取 n=1e5、|值|<=1e4（Python 参考解约 0.2s）。"""
    r = random.Random(20744)
    fmt = lambda a: ",".join(map(str, a)) + "\n"
    out = [
        "7\n", "-7\n", "0\n",                      # n=1
        "-2,-2,-2\n",                               # 题面第二个样例：全负，只能取一个
        "-5,-1,-8,-3\n",                            # 全负，答案是最大元素
        "0,0,0,0\n",
        "3,-100,4\n",                               # 放回中间的大负数
        "-1,5\n", "5,-1\n", "10,-1,-1,10\n",      # 只能放回一个
        "1,2,3,4,5\n",                              # 全正，不放回
        "-3,8,-20,6,-1,7,-50,9\n",
    ]
    for n in (50, 200, 1000):
        out.append(fmt([r.randint(-50, 40) for _ in range(n)]))
    out.append(fmt([r.randint(-10000, -1) for _ in range(100000)]))   # 全负大规模
    out.append(fmt([r.randint(-10000, 10000) for _ in range(100000)]))
    out.append(fmt([r.randint(-10000, 9000) for _ in range(100000)]))
    a = [r.randint(1, 10000) for _ in range(100000)]
    for k in range(0, 100000, 5000):
        a[k] = -10000                                # 正数海洋里插大负数
    out.append(fmt(a))
    return out


def main():
    assert SAMPLE_IN == '1,-5,0,3\n'
    cases = [SAMPLE_IN]
    for index in range(1, 20):
        for attempt in range(100):
            content = generate_case(random.Random(20744 + index + attempt * 1000))
            if content not in cases: break
        else: raise AssertionError('insufficient diversity')
        cases.append(content)
    for content in extra_cases():
        assert content not in cases
        cases.append(content)
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        root.mkdir(exist_ok=True)
        for index, content in enumerate(cases):
            assert valid(content), index
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
    assert (root / "0.out").read_text() == SAMPLE_OUT


if __name__ == "__main__":
    main()
