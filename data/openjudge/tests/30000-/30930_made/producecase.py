import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "import sys\n\ndef solve():\n    # 一次性读取所有输入，提升读取效率\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    n = int(input_data[0])\n    # 将发言数转换为整数列表\n    x = [int(v) for v in input_data[1:n+1]]\n    \n    # 将发言数量从大到小排序\n    x.sort(reverse=True)\n    \n    h_index = 0\n    # 遍历排序后的数组，寻找最大的满足条件的 k\n    for i in range(n):\n        if x[i] >= i + 1:\n            h_index = i + 1\n        else:\n            break\n            \n    print(h_index)\n\nif __name__ == '__main__':\n    solve()\n"
SAMPLE_IN = '22\n262 128 210 223 62 70 104 61 80 44 40 6 63 94 42 18 1 13 0 0 0 0\n'
def generate_case(r):
    n = r.randint(1, 80); values = [r.randint(0, 1000) for _ in range(n)]
    return f"{n}\n" + " ".join(map(str, values)) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(30930 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
