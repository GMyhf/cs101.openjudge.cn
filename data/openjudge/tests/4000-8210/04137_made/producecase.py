def solve_text(text):
    it = iter(text.split()); out = []
    for _ in range(int(next(it))):
        number, remove = next(it), int(next(it)); stack = []
        for ch in number:
            while stack and remove and stack[-1] > ch:
                stack.pop(); remove -= 1
            stack.append(ch)
        if remove: stack = stack[:-remove]
        out.append("".join(stack).lstrip("0") or "0")
    return "\n".join(out) + "\n"


def generate_case(rng):
    cases = [("9128456", 2), ("1444", 3), ("987654321", 4), ("100000001", 2)]
    for _ in range(12):
        size = rng.randint(2, 9)
        cases.append((str(rng.randint(1, 9)) + "".join(str(rng.randint(1, 9)) for _ in range(size - 1)), rng.randint(1, size - 1)))
    return str(len(cases)) + "\n" + "\n".join(f"{n} {k}" for n, k in cases) + "\n"

import random
from pathlib import Path
SAMPLE_IN = '2\n9128456 2\n1444 3\n'
SAMPLE_OUT = '12456\n1\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(4137)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 04137")
