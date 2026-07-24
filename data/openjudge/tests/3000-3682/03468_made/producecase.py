def solve_text(text):
    it = iter(text.split()); out = []
    while True:
        try: n = int(next(it))
        except StopIteration: break
        v = [int(next(it)) for _ in range(n)]
        total, largest = sum(v), max(v)
        out.append(f"{min(total / 2, total - largest):.1f}")
    return "\n".join(out) + ("\n" if out else "")


def generate_case(rng):
    cases = [[3, 5], [3, 3, 5], [2, 2], [1, 9, 9, 9, 9]]
    cases += [[rng.randint(1, 30) for _ in range(rng.randint(2, 8))] for _ in range(8)]
    return "\n".join(str(len(v)) + "\n" + " ".join(map(str, v)) for v in cases) + "\n"

import random
from pathlib import Path
SAMPLE_IN = '2\n3 5\n3\n3 3 5\n'
SAMPLE_OUT = '3.0\n5.5\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(3468)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 03468")
