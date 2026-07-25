"""12757 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 12757
SAMPLE_IN = 'negative seven hundred twenty nine\n'
SAMPLE_OUT = '-729\n'
REFERENCE_SOURCE = '# 焦玮宸 24数学科学学院\ndictionary = {\'zero\': 0, \'one\': 1, \'two\': 2, \'three\': 3, \'four\': 4, \'five\': 5, \'six\': 6, \'seven\': 7, \'eight\': 8, \'nine\': 9, \'ten\': 10, \'eleven\': 11, \'twelve\': 12, \'thirteen\': 13, \'fourteen\': 14, \'fifteen\': 15, \'sixteen\': 16, \'seventeen\': 17, \'eighteen\': 18, \'nineteen\': 19, \'twenty\': 20, \'thirty\': 30, \'forty\': 40, \'fifty\': 50, \'sixty\': 60, \'seventy\': 70, \'eighty\': 80, \'ninety\': 90}\ndef convert(words):\n    if words[0] == "negative":\n        return -convert(words[1:])\n    if "million" in words:\n        ind = words.index("million")\n        return convert(words[:ind]) * (10 ** 6) + (convert(words[ind + 1:]) if ind < len(words) - 1 else 0)\n    if "thousand" in words:\n        ind = words.index("thousand")\n        return convert(words[:ind]) * (10 ** 3) + (convert(words[ind + 1:]) if ind < len(words) - 1 else 0)\n    if "hundred" in words:\n        ind = words.index("hundred")\n        return convert(words[:ind]) * (10 ** 2) + (convert(words[ind + 1:]) if ind < len(words) - 1 else 0)\n    return sum(list(map(lambda s: dictionary[s], words)))\n\n\nprint(convert(list(input().split())))\n'

ONES = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

TEENS = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']

TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

def number_words(n):
    if n < 0: return "negative " + number_words(-n)
    if n < 10: return ONES[n]
    if n < 20: return TEENS[n - 10]
    if n < 100: return TENS[n // 10] + ((" " + ONES[n % 10]) if n % 10 else "")
    if n < 1000: return ONES[n // 100] + " hundred" + ((" " + number_words(n % 100)) if n % 100 else "")
    if n < 1_000_000: return number_words(n // 1000) + " thousand" + ((" " + number_words(n % 1000)) if n % 1000 else "")
    return number_words(n // 1_000_000) + " million" + ((" " + number_words(n % 1_000_000)) if n % 1_000_000 else "")

def g12757(r):
    return number_words(r.randint(-9_999_999, 9_999_999)) + "\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g12757(random.Random(NUMBER + i + attempt * 1000))
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
