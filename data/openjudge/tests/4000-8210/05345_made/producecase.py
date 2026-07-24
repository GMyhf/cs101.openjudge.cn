def solve_text(text):
    it = iter(text.split()); n, m = int(next(it)), int(next(it))
    values = [int(next(it)) for _ in range(n)]; out = []
    for _ in range(m):
        op, x = next(it), int(next(it))
        if op == "C": values = [(v + x) % 65536 for v in values]
        else: out.append(str(sum((v >> x) & 1 for v in values)))
    return "\n".join(out) + ("\n" if out else "")


def generate_case(rng):
    n, m = rng.randint(1, 20), rng.randint(20, 60)
    values = [rng.randrange(65536) for _ in range(n)]
    ops = [(rng.choice(["C", "C", "Q"]), rng.randrange(16)) for _ in range(m)]
    return f"{n} {m}\n" + " ".join(map(str, values)) + "\n" + "\n".join(f"{op} {x}" for op, x in ops) + "\n"

import random
from pathlib import Path
SAMPLE_IN = '3 5\n1 2 4\nQ 1\nQ 2\nC 1\nQ 1\nQ 2\n'
SAMPLE_OUT = '1\n1\n2\n1\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(5345)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 05345")
