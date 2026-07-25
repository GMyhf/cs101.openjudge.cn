import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'from collections import defaultdict\nn,m1,m2=map(int,input().split())\nd=defaultdict(int)\nl1,l2=[],[]\nfor i in range(m1):\n    l1.append(tuple(map(int,input().split())))\nfor i in range(m2):\n    l2.append(tuple(map(int,input().split())))\nfor i in range(m1):\n    for j in range(m2):\n        if l1[i][1]==l2[j][0]:\n            d[(l1[i][0],l2[j][1])]+=l1[i][2]*l2[j][2]\nfor i in range(n):\n    for j in range(n):\n        if d[(i,j)]:\n            print(i,j,d[(i,j)])\n'
SAMPLE_IN = '3 3 2\n0 0 1\n1 0 -1\n1 2 3\n0 0 7\n2 2 1\n'
def generate_case(r):
    n = r.randint(2, 8); cells = [(i, j) for i in range(n) for j in range(n)]
    r.shuffle(cells); m1 = r.randint(1, min(12, len(cells))); xcells = cells[:m1]
    r.shuffle(cells); m2 = r.randint(1, min(12, len(cells))); ycells = cells[:m2]
    if not any(j == k for _, j in xcells for k, _ in ycells):
        xcells[0] = (xcells[0][0], ycells[0][0])
    xv = [(i, j, r.choice([x for x in range(-9, 10) if x])) for i, j in xcells]
    yv = [(i, j, r.choice([x for x in range(-9, 10) if x])) for i, j in ycells]
    assert len({(i, j) for i, j, _ in xv}) == m1 and len({(i, j) for i, j, _ in yv}) == m2
    assert all(v != 0 and 0 <= i < n and 0 <= j < n for i, j, v in xv + yv)
    return f"{n} {m1} {m2}\n" + "\n".join(f"{i} {j} {v}" for i, j, v in xv + yv) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(23555 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
