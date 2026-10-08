"""20453 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import re
import subprocess
import tempfile
from pathlib import Path

NUMBER = 20453
SAMPLE_IN = '1 1 1\n2\n'
SAMPLE_OUT = '2\n'
REFERENCE_SOURCE = 'def subarray_sum(nums, k):\n    count = 0\n    sums = 0\n    d = dict()\n    d[0] = 1\n\n    for i in range(len(nums)):\n        sums += nums[i]\n        count += d.get(sums - k, 0)\n        d[sums] = d.get(sums, 0) + 1\n\n    return count\n\nnums = list(map(int, input().split()))\nk = int(input().strip())\nprint(subarray_sum(nums, k))\n'

def g20453(r):
    a=[r.randint(-5,8) for _ in range(r.randint(2,20))]; return " ".join(map(str,a))+"\n"+str(r.randint(-8,15))+"\n"

INT_RE = re.compile(r"-?(0|[1-9][0-9]*)")


def valid(text):
    """题面契约：第一行是空格分隔的一组整数（至少一个），第二行是整数 k，恰两行。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    nums = lines[0].split(" ")
    if not nums or not all(INT_RE.fullmatch(t) for t in nums):
        return False
    return INT_RE.fullmatch(lines[1]) is not None


def extra_cases():
    """补充：最小规模、全零（答案很大）、满规模随机（卡 O(n^2) 枚举）。"""
    r = random.Random(NUMBER * 7 + 1)
    out = []
    out.append("5\n5\n")                     # n=1，命中
    out.append("-3\n4\n")                    # n=1，不命中，答案 0
    out.append(" ".join(["0"] * 20000) + "\n0\n")  # 全零 k=0，答案 n(n+1)/2
    for k in (0, 7, -1000):
        a = [r.randint(-1000, 1000) for _ in range(100000)]
        out.append(" ".join(map(str, a)) + "\n" + str(k) + "\n")
    a = [r.randint(-2, 2) for _ in range(100000)]  # 小值域满规模，答案较大
    out.append(" ".join(map(str, a)) + "\n1\n")
    return out


def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20453(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    for value in extra_cases():
        assert value not in cases
        cases.append(value)
    for value in cases:
        assert valid(value), "生成的数据越出题面约束"
    return cases

def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
