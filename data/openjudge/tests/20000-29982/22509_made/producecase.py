import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'from math import log2\n\ndef find_x(y):\n    # 定义方程\n    def equation(x):\n        return x**2 + x + 1 + log2(x)\n\n    # 二分查找解\n    left, right = 0, y  # x的解显然在0和y之间，因为当x=y时，x^2 + x + 1 + log2(x) > y\n    while right - left > 1e-8:  # 精确到小数点后8位\n        mid = (left + right) / 2\n        if equation(mid) < y:\n            left = mid\n        else:\n            right = mid\n    return (left + right) / 2\n\n# 主程序开始\n# 读取输入并计算答案\nresults = []\ntry:\n    while True:\n        y = int(input())\n        x = find_x(y)\n        results.append(x)\nexcept EOFError:\n    pass\n\n# 输出结果\nfor x in results:\n    print(f"{x:.4f}")\n'
SAMPLE_IN = '10\n49\n'
SAMPLE_OUT = '2.3333\n6.2532\n'
def generate_case(r):
    values = [r.randint(10, 100000000) for _ in range(r.randint(2, 10))]
    assert all(10 <= y <= 100000000 for y in values)
    return "\n".join(map(str, values)) + "\n"

def valid(text):
    """题面：多组测试用例，每组一行，一个正整数 y（10≤y≤100000000）。"""
    if not text.endswith("\n") or text == "\n":
        return False
    for line in text[:-1].split("\n"):
        if not line.isdigit() or line != str(int(line)) or not 10 <= int(line) <= 100000000:
            return False
    return True


def safe(y):
    """解离四舍五入到 4 位小数的边界足够远（> 1e-3 个末位单位），避免浮点误差导致答案不唯一。"""
    from decimal import Decimal as D, localcontext
    with localcontext() as ctx:
        ctx.prec = 50
        ln2 = D(2).ln(); Y = D(y); x = Y.sqrt()
        for _ in range(200):
            nx = x - (x * x + x + 1 + x.ln() / ln2 - Y) / (2 * x + 1 + 1 / (x * ln2))
            if abs(nx - x) < D(10) ** -40: x = nx; break
            x = nx
        return abs((x * 10000) % 1 - D("0.5")) > D("0.001")


def many(r, cnt, lo, hi):
    out = []
    while len(out) < cnt:
        y = r.randint(lo, hi)
        if safe(y): out.append(y)
    return "\n".join(map(str, out)) + "\n"


def main():
    assert SAMPLE_IN == '10\n49\n'
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        cases = []
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(22509 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError('insufficient diversity')
            seen.append(content)
            cases.append(content)
        # 补充：上下界、小 y 密集、大量用例（每行一个 y，组数不设上限，卡掉每次都慢速求解的写法）
        bounds = [y for y in [10, 11, 12, 13, 100000000, 99999999, 99999998] if safe(y)]
        cases.append("\n".join(map(str, bounds)) + "\n")
        cases.append(many(random.Random(2250901), 300, 10, 1000))
        cases.append(many(random.Random(2250902), 2000, 10, 100000000))
        cases.append(many(random.Random(2250903), 10000, 10, 100000000))
        assert len(set(cases)) == len(cases)
        for index, content in enumerate(cases):
            assert valid(content), index
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
