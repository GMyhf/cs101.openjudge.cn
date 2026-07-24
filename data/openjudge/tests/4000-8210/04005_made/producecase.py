import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '3\n92 83 71\n95 87 74\n2\n20 20\n20 20\n2\n20 19\n22 18\n0\n'
SAMPLE_OUT = '9 5\n4 4\n4 4\n'
CASES = ['3\n92 83 71\n95 87 74\n2\n20 20\n20 20\n2\n20 19\n22 18\n0\n', '11\n44 17 88 12 86 78 4 53 18 44 63\n86 58 88 98 78 77 55 84 72 78 73\n5\n75 14 24 27 89\n55 9 74 92 33\n11\n19 92 7 6 36 48 5 94 51 4 37\n34 85 51 15 9 4 93 4 84 67 97\n0\n', '5\n17 21 50 8 54\n77 81 28 17 49\n8\n93 77 68 7 61 6 29 85\n33 41 7 12 76 95 86 97\n12\n89 29 20 2 69 26 4 2 80 77 36 100\n14 49 80 73 75 86 45 41 51 22 74 38\n0\n', '12\n35 44 15 6 86 59 55 83 59 49 25 10\n74 23 51 59 93 82 39 55 30 88 49 32\n2\n50 60\n5 48\n0\n', '1\n1\n39\n2\n75 56\n34 23\n6\n6 18 45 18 17 35\n69 13 53 61 98 18\n1\n69\n93\n3\n29 6 87\n67 11 41\n0\n', '5\n66 39 81 88 3\n56 97 50 22 78\n8\n29 69 33 77 88 48 99 51\n34 89 10 83 21 89 87 9\n8\n22 26 88 11 19 18 21 5\n14 75 8 29 45 37 22 11\n0\n', '7\n82 17 26 98 61 81 26\n12 42 22 76 89 77 6\n7\n83 39 68 54 84 49 40\n38 87 52 75 67 23 39\n0\n', '10\n82 39 25 4 10 87 10 1 72 74\n23 24 72 56 31 76 32 77 75 62\n10\n11 21 30 18 86 28 48 42 99 95\n100 68 44 12 83 58 85 42 43 37\n10\n98 68 54 78 55 76 50 66 83 77\n84 25 82 60 65 7 12 98 34 27\n0\n', '6\n58 46 38 59 87 82\n44 69 96 32 31 47\n9\n95 91 19 30 44 97 61 55 52\n52 95 19 95 36 29 51 92 51\n0\n', '10\n79 98 74 17 93 92 24 49 98 8\n30 29 95 34 65 4 79 67 6 37\n9\n89 85 39 64 33 6 11 17 19\n28 27 46 43 18 49 24 50 41\n4\n12 42 100 22\n78 26 12 33\n2\n75 51\n62 51\n12\n42 27 51 37 61 5 56 52 95 68 88 14\n27 6 45 30 30 17 53 75 67 37 28 29\n0\n', '5\n3 23 46 52 8\n21 21 77 47 91\n10\n49 91 27 22 21 78 27 94 66 49\n85 70 75 53 33 86 98 6 6 61\n11\n43 93 23 9 14 2 49 96 82 35 14\n1 67 67 21 45 46 14 65 36 76 40\n4\n86 75 51 100\n94 75 57 35\n7\n55 21 91 7 25 26 1\n53 83 72 48 63 93 21\n0\n', '6\n21 76 29 93 55 93\n10 6 92 56 15 32\n10\n10 13 28 32 100 70 63 5 64 8\n83 67 71 92 49 53 70 51 17 96\n1\n79\n56\n0\n', '6\n100 92 53 29 10 100\n34 14 34 44 41 83\n9\n39 42 81 11 96 43 6 48 57\n78 15 22 47 89 77 55 91 54\n2\n90 27\n82 46\n4\n79 7 30 56\n81 20 32 86\n0\n', '2\n70 50\n97 92\n9\n60 12 65 81 65 9 1 90 87\n21 95 96 61 55 85 82 80 1\n6\n14 19 20 43 67 43\n67 56 75 66 60 50\n11\n71 22 14 16 40 71 97 17 28 14 4\n48 59 82 23 11 16 38 82 40 36 91\n8\n59 38 33 46 97 23 17 59\n84 79 11 62 44 4 78 50\n0\n', '11\n99 58 83 87 46 15 30 57 68 96 50\n79 51 69 65 2 51 7 81 37 33 67\n5\n11 20 37 54 23\n48 34 42 38 41\n6\n24 60 1 63 18 29\n73 61 4 8 24 93\n11\n40 99 67 85 66 93 34 9 24 25 92\n76 70 37 94 68 54 84 59 51 88 5\n0\n', '12\n27 87 56 34 68 98 59 91 65 10 28 35\n71 30 55 76 20 95 7 36 54 26 6 14\n2\n2 21\n11 97\n2\n42 80\n17 74\n0\n', '12\n46 100 34 6 2 9 16 100 7 70 30 33\n44 13 50 41 46 20 9 38 17 27 88 21\n7\n71 23 9 11 76 15 23\n6 88 41 77 81 15 5\n0\n', '2\n36 52\n25 89\n12\n82 40 60 26 48 19 69 16 80 59 84 14\n98 19 71 68 65 38 65 19 99 94 29 7\n8\n52 64 93 53 85 96 41 60\n44 26 33 1 61 64 58 5\n10\n30 45 38 41 9 2 43 32 19 63\n100 41 4 91 41 90 12 36 26 18\n0\n', '8\n1 13 74 12 47 80 56 16\n75 90 58 64 66 49 94 25\n10\n64 21 58 1 11 71 59 45 93 55\n64 67 36 27 64 2 28 72 32 68\n8\n55 5 67 52 15 52 34 53\n5 54 43 28 94 78 86 27\n5\n64 69 90 19 23\n27 74 5 34 86\n11\n70 39 47 36 83 48 80 10 71 57 58\n64 91 48 26 100 33 25 90 7 18 77\n0\n', '12\n5 50 38 14 84 62 55 61 80 55 20 92\n42 92 48 56 72 67 19 54 91 43 80 71\n5\n72 63 18 98 48\n68 93 91 96 29\n6\n76 81 76 62 68 34\n75 56 59 53 45 89\n3\n5 29 69\n8 80 34\n0\n']
REFERENCE_SOURCE = 'def get_max_profit(a1, a2):\n    la1 = 0\n    ra1 = len(a1) - 1\n    la2 = 0\n    ra2 = len(a2) - 1\n    ans_max = 0\n    ans_min = 0\n\n    while la2 <= ra2:\n        if a2[la2] > a1[la1]:\n            ans_max += 3\n            ans_min += 1\n            la1 += 1\n            la2 += 1\n        elif a2[ra2] > a1[ra1]:\n            ans_max += 3\n            ans_min += 1\n            ra1 -= 1\n            ra2 -= 1\n        else:\n            if a2[la2] < a1[ra1]:\n                ans_max += 1\n                ans_min += 3\n            elif a2[la2] == a1[ra1]:\n                ans_max += 2\n                ans_min += 2\n\n            la2 += 1\n            ra1 -= 1\n\n    return ans_max, ans_min\n\n\nwhile True:\n    n = int(input())\n    if n == 0:\n        break\n\n    *C, = map(int, input().split())\n    *S, = map(int, input().split())\n    C.sort()\n    S.sort()\n\n    ans_max, _ = get_max_profit(C, S)\n    _, ans_min = get_max_profit(S, C)\n\n    print(ans_max, ans_min)\n'
assert SAMPLE_IN.strip()
assert SAMPLE_OUT.strip()
random.seed(4005)
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
