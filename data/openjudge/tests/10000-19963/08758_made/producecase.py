"""8758 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 8758
SAMPLE_IN = '137\n'
SAMPLE_OUT = '2(2(2)+2+2(0))+2(2+2(0))+2(0)\n'
REFERENCE_SOURCE = "def power_of_two_representation(n):\n    # 函数用于找到小于或等于n的最大2的幂次\n    def find_max_power(n):\n        power = 0\n        while (1 << power) <= n:\n            power += 1\n        return power - 1\n\n    # 函数用于将幂次表示为2的幂次方的表示\n    def represent_power(power):\n        if power == 1:\n            return '2'\n        elif power == 0:\n            return '2(0)'\n        else:\n            return '2(' + power_of_two_representation(power) + ')'\n\n    # 特殊情况：如果n是0，直接返回空字符串\n    if n == 0:\n        return ''\n\n    result = ''\n    while n > 0:\n        max_power = find_max_power(n)\n        # 如果结果字符串不为空，添加加号\n        if result:\n            result += '+'\n        # 把最大幂次转换为2的幂次方的表示\n        result += represent_power(max_power)\n        # 减去已经表示的数，继续寻找余数的表示\n        n -= 1 << max_power\n\n    return result\n\nprint(power_of_two_representation(int(input())))\n"

def g8758(r):
    return str(r.randint(1, 20000)) + "\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g8758(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
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
