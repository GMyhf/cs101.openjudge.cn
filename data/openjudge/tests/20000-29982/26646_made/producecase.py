import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '# 23n2300011072(X)\ndef generate_intervals(x, width, m):\n    temp = []\n    for start in range(max(0, x-width+1), min(m, x+1)):\n        end = start+width\n        if end <= m:\n            temp.append((start, end))\n    return temp\n\n\nn, m = map(int, input().split())\nplans = [tuple(map(int, input().split())) for _ in range(n)]\nintervals = []\nfor x, width in plans:\n    intervals.extend(generate_intervals(x, width, m))\nintervals.sort(key=lambda x: (x[1], x[0]))\ncnt = 0\nlast_end = 0\nfor start, end in intervals:\n    if start >= last_end:\n        last_end = end\n        cnt += 1\nprint(cnt)\n'
SAMPLE_IN = '3 5\n0 1\n3 2\n3 2\n'
SAMPLE_OUT = '2\n'
def valid(text):
    """题面：首行 n m（n, m <= 1000，取正整数）；之后 n 行 x[i] y[i]，
    x[i] 从小到大（非降，样例有相等）且在 [0, m) 内，y[i] > 0。"""
    if not text.endswith("\n"):
        return False
    lines = text.split("\n")[:-1]
    def ints(line, k):
        tok = line.split()
        if len(tok) != k or " ".join(tok) != line:
            return None
        try:
            v = [int(t) for t in tok]
        except ValueError:
            return None
        if any(str(x) != t for x, t in zip(v, tok)):
            return None
        return v
    if not lines:
        return False
    head = ints(lines[0], 2)
    if head is None:
        return False
    n, m = head
    if not (1 <= n <= 1000 and 1 <= m <= 1000) or len(lines) != n + 1:
        return False
    prev = -1
    for line in lines[1:]:
        v = ints(line, 2)
        if v is None:
            return False
        x, y = v
        if not (0 <= x < m) or x < prev or y <= 0:
            return False
        prev = x
    return True

def _build(r, n, m, ymode):
    rows = []
    for _ in range(n):
        x = r.randrange(m)
        if ymode == "small":
            y = r.randint(1, max(1, min(m, 5)))
        elif ymode == "mid":
            y = r.randint(1, max(1, m // 4))
        elif ymode == "big":
            y = r.randint(max(1, m // 2), m)
        elif ymode == "over":  # 混入 y > m 或放不下的需求
            y = r.choice([r.randint(1, m), m + r.randint(1, 50), r.randint(1, m)])
        else:  # mix
            y = r.choice([1, 2, r.randint(1, m), r.randint(1, max(1, m // 3)), m])
        rows.append((x, y))
    rows.sort(key=lambda p: p[0])
    return f"{n} {m}\n" + "\n".join(f"{x} {y}" for x, y in rows) + "\n"

def generate_case(r, index):
    modes = ["small", "mid", "big", "over", "mix"]
    if index <= 10:  # 小规模，便于暴力核对
        m = r.randint(1, 12); n = r.randint(1, 9)
        return _build(r, n, m, modes[index % 5])
    if index == 11:  # 最小规模
        return "1 1\n0 1\n"
    if index == 12:  # 唯一需求放不下
        return "1 5\n2 6\n"
    if index == 13:  # 满规模，宽度 1、x 全不同：答案 1000
        return "1000 1000\n" + "\n".join(f"{i} 1" for i in range(1000)) + "\n"
    if index == 14:  # 满规模，全挤在同一点
        return "1000 1000\n" + "\n".join("500 1" for _ in range(1000)) + "\n"
    if index == 15:  # n 远大于 m
        return _build(r, 1000, 10, "small")
    if index == 16:  # 满规模，宽度适中、可左右挪动
        return "1000 1000\n" + "\n".join(f"{i} {r.randint(1, 3)}" for i in range(1000)) + "\n"
    if index == 17:  # 满规模，候选区间最多（参考解最慢）
        return "1000 1000\n" + "\n".join("500 500" for _ in range(1000)) + "\n"
    m = r.choice([1000, r.randint(300, 1000)]); n = r.choice([1000, r.randint(100, 1000)])
    return _build(r, n, m, modes[index % 5])

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(20):
            if index == 0: content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(26646 + index + attempt * 1000), index)
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
