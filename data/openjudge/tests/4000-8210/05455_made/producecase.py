def solve_text(text):
    values = list(dict.fromkeys(map(int, text.split())))
    if not values: return ""
    left, right = {}, {}
    for value in values[1:]:
        cur = values[0]
        while True:
            if value < cur:
                if cur not in left: left[cur] = value; break
                cur = left[cur]
            elif value > cur:
                if cur not in right: right[cur] = value; break
                cur = right[cur]
            else: break
    queue = [values[0]]; out = []
    while queue:
        cur = queue.pop(0); out.append(str(cur))
        if cur in left: queue.append(left[cur])
        if cur in right: queue.append(right[cur])
    return " ".join(out) + "\n"


def generate_case(rng): return " ".join(map(str, rng.sample(range(1, 200), rng.randint(3, 30)) + [1, 1, 2])) + "\n"

import random
from pathlib import Path
SAMPLE_IN = '51 45 59 86 45 4 15 76 60 20 61 77 62 30 2 37 13 82 19 74 2 79 79 97 33 90 11 7 29 14 50 1 96 59 91 39 34 6 72 7\n'
SAMPLE_OUT = '51 45 59 4 50 86 2 15 76 97 1 13 20 60 77 90 11 14 19 30 61 82 96 7 29 37 62 79 91 6 33 39 74 34 72\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(5455)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 05455")
