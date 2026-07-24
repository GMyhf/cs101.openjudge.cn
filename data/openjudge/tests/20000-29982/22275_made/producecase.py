def solve_text(text):
    values = list(map(int, text.split())); preorder = values[1:]; postorder = []
    def visit(sequence):
        if not sequence: return
        root = sequence[0]; cut = 1
        while cut < len(sequence) and sequence[cut] < root: cut += 1
        visit(sequence[1:cut]); visit(sequence[cut:]); postorder.append(str(root))
    visit(preorder)
    return " ".join(postorder) + "\n"


def generate_case(rng):
    n = rng.randint(1, 80); values = list(range(1, n + 1)); rng.shuffle(values)
    return f"{n}\n" + " ".join(map(str, values)) + "\n"

import random
from pathlib import Path
SAMPLE_IN = '5\n4 2 1 3 5\n'
SAMPLE_OUT = '1 3 2 5 4\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(22275)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 22275")
