import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '1\n2\n1 2\n3 4\n'
SAMPLE_OUT = '3 1\n4 2\n'
CASES = ['1\n2\n1 2\n3 4\n', '2\n4\n9 3 -6 3\n8 -3 -3 5\n5 9 -5 1\n-6 -7 -3 5\n7\n5 6 -3 1 1 -5 0\n-3 4 1 3 6 8 3\n-1 3 -6 -5 -6 -1 -7\n-3 -3 -2 -6 7 4 1\n3 3 -9 6 -5 0 7\n-2 8 -2 -6 -1 4 8\n-3 -5 1 7 -3 -9 4\n', '3\n5\n-4 3 4 9 7\n4 -4 -6 -9 -8\n-9 2 -9 3 8\n1 -2 1 -6 -2\n4 6 4 -8 -4\n7\n4 -9 -1 -6 -7 9 2\n7 -2 0 3 4 -5 2\n3 -4 -9 -4 -5 -9 -3\n-6 1 7 -8 3 4 5\n-9 -4 -6 9 -7 2 -9\n-5 -2 -8 -7 4 -6 1\n-2 3 -3 2 9 -5 0\n3\n-3 -6 -2\n-8 -8 -6\n3 -8 6\n', '1\n5\n-4 -9 3 1 -3\n-2 -1 -6 -6 4\n1 8 6 0 7\n2 -2 4 8 1\n9 -4 0 -6 6\n', '2\n4\n-4 3 8 -3\n2 4 -4 6\n-6 -4 -7 1\n-4 5 -7 2\n4\n-9 -3 -7 9\n9 -6 -9 -3\n3 -5 -5 -5\n5 -2 7 0\n', '4\n7\n6 9 2 -2 0 5 6\n1 6 -4 4 5 0 1\n-5 5 2 -1 -6 3 -1\n-1 -3 9 1 2 1 -3\n8 -4 -9 9 8 0 -1\n-4 5 -3 -2 -5 7 3\n-3 -6 8 -5 -6 -6 -3\n6\n1 -5 4 6 3 -6\n2 -8 -5 -1 -7 -2\n5 2 -6 -5 9 -5\n5 7 8 -3 -3 -9\n-1 2 2 0 8 -3\n-1 -5 -3 2 5 8\n1\n-7\n4\n0 6 6 -9\n0 -9 -7 -2\n-2 6 -1 2\n3 -7 8 -8\n', '3\n6\n-9 0 8 -6 -6 -4\n4 -4 1 -7 3 -9\n0 4 0 -4 7 1\n0 3 5 -1 -8 2\n-3 3 -3 -5 1 6\n-1 -9 -6 2 -6 6\n7\n0 6 0 -1 5 -2 5\n-1 -6 -9 5 4 0 5\n2 -6 -5 -2 7 -4 -6\n1 5 -7 -3 -6 7 5\n1 -7 -6 -6 3 5 5\n-2 -9 2 -6 1 -3 7\n-2 -3 -5 4 -7 2 -4\n8\n-9 -3 -9 2 7 8 -7 -9\n1 -6 -8 6 6 4 -4 -7\n3 -1 8 0 6 2 -9 -5\n9 1 -1 7 2 -8 -7 3\n5 -6 4 4 -6 -3 -5 -5\n-3 -3 -9 3 -2 5 -7 -8\n9 8 7 1 -4 7 -2 7\n4 -9 9 7 9 0 -2 -1\n', '2\n2\n1 -8\n-5 4\n4\n-1 8 6 -2\n8 -3 -7 3\n5 8 -4 8\n-5 -9 8 5\n', '4\n3\n-5 3 3\n2 8 3\n1 -4 0\n8\n6 9 1 -2 -8 5 -3 -6\n5 9 0 7 9 3 -8 -6\n0 -8 6 5 5 -3 -3 -8\n-7 2 7 -6 5 6 -3 7\n-5 1 -3 -8 1 1 -8 -4\n4 9 -7 -6 -5 6 2 -9\n-2 0 -4 -1 -8 3 7 -6\n9 -6 -9 3 0 -6 -6 -7\n3\n-5 -2 2\n5 -7 -7\n-4 6 4\n1\n7\n', '2\n3\n-3 5 -1\n3 8 2\n1 -5 -1\n4\n5 -8 2 8\n6 2 -1 -8\n5 -2 -8 -1\n-1 -1 8 -6\n', '4\n3\n5 5 -9\n5 -8 8\n-8 3 4\n7\n-8 -2 -1 -4 -3 -5 -3\n-8 -7 0 -9 5 3 7\n2 -9 -1 7 4 5 -3\n-2 5 8 5 -2 1 -5\n5 -6 -2 -1 -6 0 -2\n-5 -7 -2 8 2 7 2\n2 8 -4 -1 2 4 -8\n6\n-6 -5 -3 -2 5 -9\n-3 7 6 6 -7 2\n0 3 -9 6 -9 5\n-3 1 0 9 9 -3\n0 7 -2 0 -1 -9\n1 9 0 -6 -2 1\n6\n-9 0 4 -8 0 -5\n-5 -4 4 -2 2 4\n2 -8 0 4 -7 -3\n7 -5 -9 -4 2 -8\n-6 0 -3 -4 4 -3\n-3 3 9 -3 -6 -5\n', '1\n8\n0 5 -2 5 6 -1 0 -1\n3 -6 6 -5 8 8 -8 -5\n9 8 5 -3 6 4 4 -7\n9 2 -8 -6 4 -2 -2 -7\n3 7 3 -5 0 -1 6 -7\n-2 9 -3 2 -1 -2 3 9\n8 -5 -7 5 8 -2 3 3\n1 6 0 7 3 -4 -7 9\n', '3\n1\n6\n1\n6\n4\n8 4 2 -6\n2 -2 1 9\n1 -7 1 3\n-9 -2 -1 -8\n', '1\n4\n-1 -6 8 -8\n8 4 -5 0\n3 -4 7 9\n9 8 -7 8\n', '2\n7\n2 0 -2 -7 2 5 -1\n-3 5 -8 1 -3 -8 -5\n7 0 3 -5 3 -3 -4\n-6 -6 -2 8 -2 7 -8\n1 -3 6 -3 3 6 3\n8 -6 8 -1 6 6 3\n-7 6 -5 7 5 8 8\n3\n4 -6 -8\n9 8 -8\n8 9 -4\n', '4\n1\n-8\n6\n3 5 7 3 3 -7\n8 -7 8 -2 4 9\n-4 2 -6 -7 -8 -6\n-2 2 3 -2 -4 0\n0 8 -4 -6 -6 -6\n-4 3 -1 6 -5 2\n7\n8 2 8 5 3 3 -8\n-1 0 -7 5 -5 -9 5\n0 -3 6 -2 4 -6 -8\n-9 -7 -9 8 -9 -8 -5\n-9 2 5 8 -4 5 -6\n0 -3 3 -6 -6 0 6\n5 -1 -7 -2 7 1 -7\n1\n8\n', '4\n3\n5 -6 6\n-1 4 -4\n-8 -6 -2\n1\n-3\n7\n-6 6 9 1 0 5 -5\n-3 5 -6 8 -3 5 6\n-2 0 -7 -6 3 -2 -9\n-1 -8 1 9 -8 -6 -1\n0 3 -1 6 -1 9 -6\n7 -3 -1 5 5 7 7\n2 -6 1 -6 2 -6 9\n4\n-2 -9 3 3\n-7 -6 5 2\n0 4 -4 -8\n1 -2 -1 1\n', '2\n2\n-2 7\n-5 4\n5\n-5 9 8 -1 -1\n-1 1 0 -8 3\n-7 9 -2 6 4\n-2 -3 -8 -2 1\n-8 5 -4 5 4\n', '4\n2\n-8 -2\n3 6\n2\n6 5\n6 -5\n3\n-9 1 -2\n4 -3 -5\n9 -6 4\n1\n-7\n', '3\n7\n0 9 -4 8 -1 -7 3\n-5 4 -3 8 -4 9 7\n-2 8 7 -4 4 5 2\n2 1 -7 9 1 0 7\n-2 2 -2 7 8 -3 -1\n-5 8 -6 -3 -6 -3 3\n2 3 -6 -6 -3 9 -4\n7\n4 8 4 -3 9 9 5\n7 9 7 0 -2 4 -7\n9 -2 4 -3 -6 -1 -6\n-3 -8 -6 -2 9 -5 7\n-9 -3 -7 2 2 1 8\n6 -5 3 8 -3 8 6\n7 -2 -7 5 9 -1 -1\n7\n-8 -8 9 4 6 6 -5\n-3 6 0 5 -9 0 -8\n-6 1 -9 -2 -4 -2 1\n2 -7 -9 -4 -8 5 -5\n1 -6 9 0 -7 -8 3\n2 -7 -1 -3 8 -1 -5\n-8 -1 -3 6 7 -9 4\n']
REFERENCE_SOURCE = 'def rotate_matrix_90(matrix):\n    n = len(matrix)\n    return [[matrix[n - j - 1][i] for j in range(n)] for i in range(n)]\n\ndef print_matrix(matrix):\n    for row in matrix:\n        print(\' \'.join(map(str, row)))\n\ndef main():\n    M = int(input())\n    results = []\n    for _ in range(M):\n        n = int(input())\n        matrix = [list(map(int, input().split())) for _ in range(n)]\n        rotated = rotate_matrix_90(matrix)\n        results.append(rotated)\n    \n    for result in results:\n        print_matrix(result)\n\nif __name__ == "__main__":\n    main()\n\n'
assert SAMPLE_IN.strip()
assert SAMPLE_OUT.strip()
random.seed(4075)
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
