#!/usr/bin/env python3
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(data[i + 1]) for i in range(n)]

    total = sum(a)
    if total % 3 != 0:
        print(0)
        return

    target = total // 3
    target2 = 2 * target

    # Count ways to split into 3 non-empty contiguous parts each summing to target
    # prefix[i] = a[0]+...+a[i-1]
    # We need prefix[i] = target (first cut after i), prefix[j] = target2 (second cut after j)
    # where 1 <= i < j <= n-1 (0-indexed: i in [1, n-2], j in [i+1, n-1])

    # Count suffix occurrences of prefix sum = target2
    # Then sweep from left

    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + a[i]

    # cnt2[i] = number of j in [i+1, n-1] such that prefix[j] == target2
    # We need j such that prefix[j] = target2 and j >= 2 and j <= n-1
    # (j is the start of the third part, so third part is a[j..n-1])

    # Actually: first part is a[0..i-1], second is a[i..j-1], third is a[j..n-1]
    # prefix[i] = target, prefix[j] = target2, 1 <= i < j <= n-1

    # Build suffix count of positions where prefix[j] = target2
    suffix_count = 0
    ans = 0
    # We iterate i from n-2 down to 1
    # First, count all j in [2, n-1] with prefix[j] = target2
    for j in range(2, n):
        if prefix[j] == target2:
            suffix_count += 1

    for i in range(1, n - 1):
        # i is a valid first cut position
        if prefix[i] == target:
            ans += suffix_count
        # Remove i+1 from suffix_count if it was counted (since next i will need j > i+1)
        if prefix[i + 1] == target2 and (i + 1) >= 2 and (i + 1) <= n - 1:
            suffix_count -= 1

    print(ans)

solve()
