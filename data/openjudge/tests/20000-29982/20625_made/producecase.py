"""20625 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 20625
SAMPLE_IN = '10101\n'
SAMPLE_OUT = '4\n'
REFERENCE_SOURCE = 'def count_balanced_substrings(s):\n    # 初始化当前字符和前一个字符的计数器\n    curr_count = 1\n    prev_count = 0\n    result = 0\n\n    # 遍历字符串的每个字符\n    for i in range(1, len(s)):\n        # 如果当前字符和前一个字符相同，增加当前计数器\n        if s[i] == s[i - 1]:\n            curr_count += 1\n        else:\n            # 如果当前字符和前一个字符不同，那么我们可以创建\n            # min(curr_count, prev_count) 个子串\n            result += min(curr_count, prev_count)\n            # 将当前计数器值赋给前一个计数器，并重置当前计数器为1\n            prev_count = curr_count\n            curr_count = 1\n\n    # 出循环后，处理最后一组字符\n    result += min(curr_count, prev_count)\n\n    return result\n\n# 测试样例输入\n#print(count_balanced_substrings("10101"))  # 输出应该是4\n#print(count_balanced_substrings("00110011"))  # 输出应该是6\nprint(count_balanced_substrings(input()))\n'

def g20625(r): return "".join(r.choice("01") for _ in range(r.randint(2,50)))+"\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20625(random.Random(NUMBER + i + attempt * 1000))
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
