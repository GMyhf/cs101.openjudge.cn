def solve_text(text):
    it = iter(text.split()); out = []
    for _ in range(int(next(it))):
        value = next(it)
        out.append("Yes" if int(value) % 19 == 0 or "19" in value else "No")
    return "\n".join(out) + "\n"


def generate_case(rng):
    values = [19, 38, 119, 190, 191, 918, 100, 200, 1000000000] + [rng.randint(1, 2000000000) for _ in range(12)]
    return str(len(values)) + "\n" + "\n".join(map(str, values)) + "\n"

import random
from pathlib import Path
SAMPLE_IN = '4\n95\n100\n3192\n2913\n'
SAMPLE_OUT = 'Yes\nNo\nYes\nNo\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(7810)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 07810")
