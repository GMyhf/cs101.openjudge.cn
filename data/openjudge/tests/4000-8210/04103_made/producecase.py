import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '2\n'
SAMPLE_OUT = '7\n'
CASES = ['2\n', '12\n', '9\n', '6\n', '6\n', '11\n', '5\n', '7\n', '12\n', '10\n', '1\n', '1\n', '3\n', '4\n', '14\n', '11\n', '2\n', '3\n', '11\n', '2\n']
REFERENCE_SOURCE = 'n = int(input())\nstep = [[1, 0], [-1, 0], [0, 1]]\nnum = 1\n\n\ndef dfs(x, y, m, visited):\n    global num\n    if m == 0:\n        return\n    visited.append([x, y])\n    num -= 1\n    for j in range(3):\n        if [x+step[j][0], y+step[j][1]] not in visited:\n            num += 1\n            lista = []\n            lista += visited\n            dfs(x+step[j][0], y+step[j][1], m-1, lista)\n\n\ndfs(0, 0, n, [])\nprint(num)\n'
assert SAMPLE_IN.strip()
assert SAMPLE_OUT.strip()
random.seed(4103)
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
