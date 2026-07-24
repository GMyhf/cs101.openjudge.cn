import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '2\n3 2 2\n1 2\n2 3\n1 3\n1 2\n5 5 2\n1 2\n1 3\n2 5\n3 5\n4 5\n1 5\n3 4\n'
SAMPLE_OUT = 'Case 1:\n1\n0\nCase 2:\n2\n1\n'
CASES = ['2\n3 2 2\n1 2\n2 3\n1 3\n1 2\n5 5 2\n1 2\n1 3\n2 5\n3 5\n4 5\n1 5\n3 4\n', '1\n14 13 8\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n12 13\n13 14\n4 3\n7 3\n9 13\n6 7\n10 12\n7 13\n1 4\n11 8\n', '1\n20 19 8\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n12 13\n13 14\n14 15\n15 16\n16 17\n17 18\n18 19\n19 20\n17 10\n8 17\n15 1\n16 9\n13 14\n10 4\n3 6\n7 16\n', '1\n20 19 6\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n12 13\n13 14\n14 15\n15 16\n16 17\n17 18\n18 19\n19 20\n4 14\n13 4\n3 4\n8 15\n20 3\n1 5\n', '1\n3 2 7\n1 2\n2 3\n3 1\n2 3\n3 1\n1 2\n1 2\n3 1\n2 3\n', '1\n2 1 1\n1 2\n1 2\n', '1\n7 6 2\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n3 7\n4 3\n', '1\n9 8 4\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n1 9\n6 2\n1 7\n9 8\n', '1\n9 8 1\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n2 7\n', '1\n12 11 6\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n4 1\n7 5\n2 6\n1 7\n1 5\n12 11\n', '1\n5 4 6\n1 2\n2 3\n3 4\n4 5\n3 4\n3 5\n3 4\n4 3\n1 4\n5 4\n', '1\n6 5 5\n1 2\n2 3\n3 4\n4 5\n5 6\n5 4\n5 2\n4 2\n5 2\n4 1\n', '1\n7 6 2\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n6 5\n2 6\n', '1\n5 4 6\n1 2\n2 3\n3 4\n4 5\n5 2\n3 4\n2 5\n3 1\n1 3\n3 5\n', '1\n5 4 8\n1 2\n2 3\n3 4\n4 5\n3 2\n5 1\n5 4\n1 2\n2 1\n1 2\n2 1\n3 2\n', '1\n20 19 4\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n12 13\n13 14\n14 15\n15 16\n16 17\n17 18\n18 19\n19 20\n16 11\n14 9\n6 19\n7 3\n', '1\n9 8 1\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n3 6\n', '1\n14 13 6\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n12 13\n13 14\n10 2\n11 9\n6 10\n1 13\n6 2\n5 13\n', '1\n18 17 8\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n12 13\n13 14\n14 15\n15 16\n16 17\n17 18\n12 18\n14 12\n14 2\n13 16\n10 6\n8 13\n17 15\n18 10\n', '1\n20 19 1\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 10\n10 11\n11 12\n12 13\n13 14\n14 15\n15 16\n16 17\n17 18\n18 19\n19 20\n9 12\n']
REFERENCE_SOURCE = 'def count_common_friends(n, m, k, friend_connections, queries):\n    # Create a dictionary to store friend connections\n    friends_dict = {}\n    for i in range(1, n + 1):\n        friends_dict[i] = set()\n\n    # Update the dictionary with friend connections\n    for i, j in friend_connections:\n        friends_dict[i].add(j)\n        friends_dict[j].add(i)\n\n    # Count common friends for each query\n    results = []\n    for i, j in queries:\n        common_friends = len(friends_dict[i].intersection(friends_dict[j]))\n        results.append(common_friends)\n\n    return results\n\n\ndef main():\n    test_cases = int(input())\n    for case in range(1, test_cases + 1):\n        n, m, k = map(int, input().split())\n        friend_connections = []\n        queries = []\n\n        # Read friend connections\n        for _ in range(m):\n            i, j = map(int, input().split())\n            friend_connections.append((i, j))\n\n        # Read queries\n        for _ in range(k):\n            i, j = map(int, input().split())\n            queries.append((i, j))\n\n        # Count common friends and output the results\n        print(f"Case {case}:")\n        results = count_common_friends(n, m, k, friend_connections, queries)\n        for result in results:\n            print(result)\n\n\nif __name__ == "__main__":\n    main()\n'
assert SAMPLE_IN.strip()
assert SAMPLE_OUT.strip()
random.seed(4109)
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
