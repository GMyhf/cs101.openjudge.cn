import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\ninput = sys.stdin.readline\n\nN, D = map(int, input().split())\nheight = [int(input()) for _ in range(N)]\n\nchecked = [False] * N\nremaining = N\nresult = []\n\nwhile remaining > 0:\t# 只要还有未处理的位置，就继续做一轮"收集组"\n    buffer = []\n    i = 0\n    # 每轮从左到右尝试把可归入当前 buffer 的未处理元素标记并收集\n    for i in range(N):\n        if checked[i]:\n            continue\n        val = height[i]\n        if not buffer:\n            # buffer 为空时，直接加入第一个未处理元素\n            buffer.append(val)\n            maxh = val\n            minh = val\n            checked[i] = True\n            remaining -= 1\n            continue\n\n        # ⚠️ “先用当前元素更新 max/min，再判断”\n        maxh = max(maxh, val)\n        minh = min(minh, val)\n\n        # 若假设把 val 加入后仍满足与极值的差 ≤ D，则真正加入\n        if maxh - val <= D and val - minh <= D:\n            buffer.append(val)\n            checked[i] = True\n            remaining -= 1\n        \n    buffer.sort()\n    result.extend(buffer)\n\nprint(*result, sep="\\n")\n'
SAMPLE_IN = '5 3\n7\n7\n3\n6\n2\n'
SAMPLE_OUT = '6\n7\n7\n2\n3\n'
def generate_case(r):
    n = r.randint(2, 45); d = r.randint(1, 40); heights = [r.randint(1, 1000) for _ in range(n)]
    assert 1 <= n <= 10**5 and 1 <= d <= 10**9 and all(1 <= x <= 10**9 for x in heights)
    return f"{n} {d}\n" + "\n".join(map(str, heights)) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(25353 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
