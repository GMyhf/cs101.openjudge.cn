import random
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent


def render(a, b):
    return f"{len(a)}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)) + "\n"


def generate(i):
    if i == 0:
        return render([4, 8, 2, 6, 2], [4, 5, 4, 1, 3])
    if i == 1:
        return render([1, 3, 2, 4], [1, 3, 2, 4])
    if i == 2:
        return render([2, 2, 2, 2], [1, 1, 1, 1])
    if i == 3:
        return render([1, 1, 1, 1], [2, 2, 2, 2])
    rng = random.Random(2732900 + i)
    n = 2 + (i * 37) % 31
    if i == 19:
        n = 200000
    if i == 20:
        n = 199999
    if i >= 19:
        a = [rng.randint(1, 10**9) for _ in range(n)]
        b = [rng.randint(1, 10**9) for _ in range(n)]
    else:
        a = [rng.randint(1, 10**9 if i % 3 == 0 else 100) for _ in range(n)]
        b = [rng.randint(1, 10**9 if i % 3 == 0 else 100) for _ in range(n)]
    return render(a, b)


for i in range(40):
    case = generate(i)
    result = subprocess.run(
        ["python3", str(ROOT / "samplecode.py")],
        input=case, text=True, capture_output=True, check=True,
    ).stdout
    (ROOT / "data" / f"{i}.in").write_text(case, encoding="utf-8")
    (ROOT / "data" / f"{i}.out").write_text(result, encoding="utf-8")
