import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\n\ndef solve():\n    # 读取所有输入并按空格切分\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    # 第一行是 n，后面是 n 个整数\n    n = int(input_data[0])\n    # 将数组元素转为整数并放入集合中\n    nums = set(map(int, input_data[1:n+1]))\n    \n    # 从最小的正整数 1 开始查找\n    res = 1\n    while res in nums:\n        res += 1\n    \n    # 输出结果\n    print(res)\n\nif __name__ == "__main__":\n    solve()\n'
SAMPLE_IN = '3\n1 2 0\n'
def generate_case(r):
    n = r.randint(1, 100); a = [r.randint(-100, 100) for _ in range(n)]
    return f"{n}\n" + " ".join(map(str, a)) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(30646 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
