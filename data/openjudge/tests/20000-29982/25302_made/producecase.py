import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def max_concurrent_connections(n, intervals):\n    events = []\n    for start, end in intervals:\n        events.append((start, 1))  # 开始 +1\n        events.append((end, -1))   # 结束 -1\n\n    # 按时间排序，时间相同时结束事件在前\n    events.sort(key=lambda x: (x[0], x[1]))\n\n    current = 0\n    max_concurrent = 0\n    for time, delta in events:\n        current += delta\n        max_concurrent = max(max_concurrent, current)\n\n    return max_concurrent\n\n# 主程序处理多组数据\nt = int(input())\nfor _ in range(t):\n    n = int(input())\n    intervals = [tuple(map(int, input().split())) for _ in range(n)]\n    print(max_concurrent_connections(n, intervals))\n\n\n'
SAMPLE_IN = '2\n2\n1 2\n2 3\n2\n1 3\n2 4\n'
SAMPLE_OUT = '1\n2\n'
def generate_case(r):
    rows = []
    for _ in range(r.randint(2, 8)):
        intervals = []
        for _ in range(r.randint(2, 12)):
            x = r.randint(0, 100); intervals.append((x, x + r.randint(1, 30)))
        rows.append([str(len(intervals))] + [f"{x} {y}" for x, y in intervals])
    return str(len(rows)) + "\n" + "\n".join("\n".join(row) for row in rows) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(25302 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
