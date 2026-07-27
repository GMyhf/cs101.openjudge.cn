# External reference: /practice/30110/statistics/
# Accepted submission: 52825154
# Source: http://cs101.openjudge.cn/practice/solution/52825154/
# License: not declared on the submission page; no license is inferred.

import sys


def solve():
    # Read all input from standard input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    s = input_data[0]

    # Count frequencies of each digit '0'-'9'
    digit_counts = [0] * 10
    for char in s:
        if "0" <= char <= "9":
            digit_counts[int(char)] += 1

    # Construct the largest number by appending digits from 9 down to 0
    result_parts = []
    for digit in range(9, -1, -1):
        if digit_counts[digit] > 0:
            result_parts.append(str(digit) * digit_counts[digit])

    # Print the final reconstructed maximum integer
    print("".join(result_parts))


if __name__ == "__main__":
    solve()