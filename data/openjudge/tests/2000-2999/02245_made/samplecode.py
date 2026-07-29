# External reference: http://cs101.openjudge.cn/practice/02245/statistics/
# Accepted submission: 51731400
# Source: http://cs101.openjudge.cn/practice/solution/51731400/
# License: not declared on the submission page; no license is inferred.

import sys
def generate_combinations(S, k, start, depth, current, results):
    if depth == 6:
        results.append(current[:])
        return
    for i in range(start, k - (6 - depth) + 1):
        current.append(S[i])
        generate_combinations(S, k, i + 1, depth + 1, current, results)
        current.pop()
def main():
    lines = sys.stdin.read().strip().splitlines()
    first_case = True
    for line in lines:
        nums = list(map(int, line.split()))
        k = nums[0]
        if k == 0:
            break
        S = nums[1:]
        if not first_case:
            print()
        first_case = False
        results = []
        generate_combinations(S, k, 0, 0, [], results)
        for comb in results:
            print(' '.join(map(str, comb)))
if __name__ == "__main__":
    main()
