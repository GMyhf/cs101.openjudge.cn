def solve_text(text):
    it = iter(text.split()); out = []
    while True:
        radius, n = int(next(it)), int(next(it))
        if radius == n == -1: break
        troops = sorted(int(next(it)) for _ in range(n)); index = 0; answer = 0
        while index < n:
            left = troops[index]
            while index < n and troops[index] <= left + radius: index += 1
            marker = troops[index - 1]
            while index < n and troops[index] <= marker + radius: index += 1
            answer += 1
        out.append(str(answer))
    return "\n".join(out) + "\n"


def generate_case(rng):
    lines = []
    for _ in range(8):
        n = rng.randint(1, 30); lines += [f"{rng.randint(0, 20)} {n}", " ".join(map(str, [rng.randint(0, 100) for _ in range(n)]))]
    return "\n".join(lines) + "\n-1 -1\n"

import random
from pathlib import Path
SAMPLE_IN = '0 3\n10 20 20\n10 7\n70 30 1 7 15 20 50\n-1 -1\n'
SAMPLE_OUT = '2\n4\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(19757)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 19757")
