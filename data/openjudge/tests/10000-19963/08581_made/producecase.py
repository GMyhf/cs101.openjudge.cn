def solve_text(text):
    preorder = text.strip(); pos = 0; inorder = []; postorder = []
    def visit():
        nonlocal pos
        char = preorder[pos]; pos += 1
        if char == ".": return
        visit(); inorder.append(char); visit(); postorder.append(char)
    visit()
    return "".join(inorder) + "\n" + "".join(postorder) + "\n"


def generate_case(rng):
    def make(depth):
        if depth == 0 or rng.random() < .25: return "."
        return rng.choice("ABCDEFGH") + make(depth - 1) + make(depth - 1)
    return make(5) + "\n"

import random
from pathlib import Path
SAMPLE_IN = 'ABD..EF..G..C..\n'
SAMPLE_OUT = 'DBFEGAC\nDFGEBCA\n'
assert solve_text(SAMPLE_IN).strip() == SAMPLE_OUT.strip()
rng = random.Random(8581)
root = Path(__file__).parent / "data"
for index, content in enumerate([SAMPLE_IN] + [generate_case(rng) for _ in range(19)]):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_text(content), encoding="utf-8")
print("generated 20 cases for 08581")
