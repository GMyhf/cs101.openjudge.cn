import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '6\n-45 22 42 -16\n-41 -27 56 30\n-36 53 -37 77\n-36 30 -75 -46\n26 -38 -10 62\n-32 -54 -6 45\n'
SAMPLE_OUT = '5\n'
CASES = ['6\n-45 22 42 -16\n-41 -27 56 30\n-36 53 -37 77\n-36 30 -75 -46\n26 -38 -10 62\n-32 -54 -6 45\n', '4\n13 16 -13 7\n5 -16 15 -18\n-16 2 -9 5\n0 -20 -1 16\n', '12\n-4 2 -1 -7\n15 -8 14 4\n-3 6 -9 16\n-7 3 -19 -18\n-19 -18 -18 -18\n17 12 17 18\n-10 0 -5 -6\n-15 -9 -7 9\n7 -10 14 12\n19 11 19 12\n11 5 2 -1\n7 -3 -18 -8\n', '2\n4 3 1 -7\n14 9 -15 -1\n', '2\n-12 17 -19 9\n16 4 -19 -18\n', '12\n-12 -9 16 0\n-6 -17 -3 10\n-12 -3 8 13\n-8 13 -2 -19\n5 -11 -2 19\n-6 -4 -3 -5\n0 -10 -5 -8\n-15 -1 -12 13\n-10 -1 -10 18\n-14 2 -13 -2\n17 18 -4 -16\n0 -17 15 -15\n', '2\n-11 10 -6 7\n2 -3 -7 -19\n', '8\n-2 -2 18 -19\n19 5 -6 -7\n-5 -7 9 19\n-10 15 -12 14\n-14 -12 -4 4\n-2 3 9 1\n2 -17 -14 9\n8 13 12 14\n', '4\n-1 -19 -8 -19\n7 -20 -18 1\n3 -11 -17 4\n19 -12 -2 -14\n', '2\n18 -10 -11 4\n-6 13 -20 -1\n', '2\n-20 5 15 10\n5 2 -10 4\n', '12\n-4 -5 -14 9\n17 -12 20 0\n14 3 15 4\n-1 -1 -11 16\n-17 7 2 6\n20 -9 19 8\n16 20 -13 9\n7 -8 -8 -12\n-14 5 8 9\n10 -2 -14 -2\n-9 -6 3 17\n16 -11 16 4\n', '4\n-5 -1 -12 -4\n20 -20 -18 20\n12 17 4 -14\n-15 -5 -4 -15\n', '2\n10 6 -6 -7\n17 7 -3 -15\n', '2\n-20 10 12 6\n-3 5 7 -4\n', '12\n10 -2 -10 14\n20 -6 -4 14\n2 -17 -11 -12\n16 18 14 -12\n18 -3 1 20\n12 7 6 -10\n19 18 0 -14\n-19 1 5 -2\n-8 15 17 12\n-3 -17 -20 12\n-11 14 7 1\n14 19 20 -7\n', '8\n20 1 15 20\n13 -4 16 -2\n-10 7 19 -14\n7 -2 -2 8\n11 -7 -4 9\n8 4 -9 -19\n-20 -20 -9 2\n18 12 15 18\n', '12\n7 -12 -13 15\n-20 -20 -17 -13\n-14 -19 -6 -2\n-4 -4 -8 19\n-9 7 -17 -10\n14 -1 6 5\n-15 15 -18 6\n-8 -9 -8 -3\n-10 -12 19 -10\n-13 -18 2 -19\n-5 -10 -20 9\n-17 -3 -12 -6\n', '4\n10 8 12 -8\n8 -16 -15 3\n-10 -15 -20 4\n-9 17 -18 -3\n', '2\n9 -19 -11 16\n8 11 -20 13\n']
REFERENCE_SOURCE = "# https://docs.python.org/3/library/array.html\nimport array as arr\n\nn = int(input())\na = arr.array('i', [0]*(n+1))\nb = arr.array('i', [0]*(n+1))\nc = arr.array('i', [0]*(n+1))\nd = arr.array('i', [0]*(n+1))\n\nfor i in range(n):\n    a[i],b[i],c[i],d[i] = map(int, input().split())\n\n\ndict1 = {}\nfor i in range(n):\n    for j in range(n):\n        if not a[i]+b[j] in dict1:\n            dict1[a[i] + b[j]] = 0\n        dict1[a[i] + b[j]] += 1\n\nans = 0\nfor i in range(n):\n    for j in range(n):\n        if -(c[i]+d[j]) in dict1:\n            ans += dict1[-(c[i]+d[j])]\n\nprint(ans)\n"
assert SAMPLE_IN.strip()
assert SAMPLE_OUT.strip()
random.seed(3441)
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
