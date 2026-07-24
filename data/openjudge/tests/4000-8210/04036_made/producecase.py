import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '1 1 3 1 2\n'
SAMPLE_OUT = '3\n'
CASES = ['1 1 3 1 2\n', '73 58 14 9 5\n', '32 44 4 1 3\n', '25 46 13 11 2\n', '8 42 20 17 3\n', '83 70 17 10 7\n', '72 5 16 5 11\n', '54 65 20 18 2\n', '85 84 19 14 5\n', '70 4 9 0 9\n', '73 71 5 4 1\n', '58 88 17 4 13\n', '73 60 19 17 2\n', '85 58 15 7 8\n', '59 63 11 0 11\n', '67 5 10 8 2\n', '72 29 19 16 3\n', '4 55 6 2 4\n', '12 18 4 1 3\n', '1 69 18 1 17\n']
REFERENCE_SOURCE = 'import math\na, b, k, n, m = map(int, input().split());\nprint((pow(a, n, 10007) * pow(b, m, 10007) * math.comb(k, m)) % 10007)\n'
assert SAMPLE_IN.strip()
assert SAMPLE_OUT.strip()
random.seed(4036)
assert CASES[0] == SAMPLE_IN
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
def generate_case(index):
    return CASES[index]
root = Path(__file__).parent / "data"
for index in range(20):
    content = generate_case(index)
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")
