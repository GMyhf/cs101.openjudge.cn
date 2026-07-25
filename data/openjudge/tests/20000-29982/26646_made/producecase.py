import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '# 23n2300011072(X)\ndef generate_intervals(x, width, m):\n    temp = []\n    for start in range(max(0, x-width+1), min(m, x+1)):\n        end = start+width\n        if end <= m:\n            temp.append((start, end))\n    return temp\n\n\nn, m = map(int, input().split())\nplans = [tuple(map(int, input().split())) for _ in range(n)]\nintervals = []\nfor x, width in plans:\n    intervals.extend(generate_intervals(x, width, m))\nintervals.sort(key=lambda x: (x[1], x[0]))\ncnt = 0\nlast_end = 0\nfor start, end in intervals:\n    if start >= last_end:\n        last_end = end\n        cnt += 1\nprint(cnt)\n'
SAMPLE_IN = '3 5\n0 1\n3 2\n3 2\n'
SAMPLE_OUT = '2\n'
def generate_case(r):
    m = r.randint(3, 80); n = r.randint(2, min(20, m)); rows = []
    for _ in range(n):
        y = r.randint(1, m); x = r.randint(y - 1, m - 1); rows.append((x, y))
    assert all(0 <= x < m and 1 <= y <= m and x - y + 1 >= 0 for x, y in rows)
    return f"{n} {m}\n" + "\n".join(f"{x} {y}" for x, y in rows) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(26646 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
