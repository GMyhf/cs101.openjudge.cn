import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'from math import log2\n\ndef find_x(y):\n    # 定义方程\n    def equation(x):\n        return x**2 + x + 1 + log2(x)\n\n    # 二分查找解\n    left, right = 0, y  # x的解显然在0和y之间，因为当x=y时，x^2 + x + 1 + log2(x) > y\n    while right - left > 1e-8:  # 精确到小数点后8位\n        mid = (left + right) / 2\n        if equation(mid) < y:\n            left = mid\n        else:\n            right = mid\n    return (left + right) / 2\n\n# 主程序开始\n# 读取输入并计算答案\nresults = []\ntry:\n    while True:\n        y = int(input())\n        x = find_x(y)\n        results.append(x)\nexcept EOFError:\n    pass\n\n# 输出结果\nfor x in results:\n    print(f"{x:.4f}")\n'
SAMPLE_IN = '10\n49\n'
SAMPLE_OUT = '2.3333\n6.2532\n'
def generate_case(r):
    values = [r.randint(10, 100000000) for _ in range(r.randint(2, 10))]
    assert all(10 <= y <= 100000000 for y in values)
    return "\n".join(map(str, values)) + "\n"

assert SAMPLE_IN == '10\n49\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(22509 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
