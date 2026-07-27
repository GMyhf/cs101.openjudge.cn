# External reference: /practice/31042/statistics/
# Accepted submission: 52824909
# Source: http://cs101.openjudge.cn/practice/solution/52824909/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # Read all lines from standard input
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    # Safely parse N and the old file lines
    idx = 0
    while idx < len(input_data) and not input_data[idx].strip().isdigit():
        idx += 1
    if idx >= len(input_data):
        return
    N = int(input_data[idx])
    idx += 1
    old_file = input_data[idx : idx + N]
    idx += N
    
    # Safely parse M and the new file lines
    while idx < len(input_data) and not input_data[idx].strip().isdigit():
        idx += 1
    if idx >= len(input_data):
        return
    M = int(input_data[idx])
    idx += 1
    new_file = input_data[idx : idx + M]
    
    # suf[i][j] stores the LCS of old_file[i:] and new_file[j:]
    suf = [[0] * (M + 1) for _ in range(N + 1)]
    
    # Fill the DP table backwards
    for i in range(N - 1, -1, -1):
        suf_i = suf[i]
        suf_i1 = suf[i+1]
        old_val = old_file[i]
        for j in range(M - 1, -1, -1):
            if old_val == new_file[j]:
                suf_i[j] = suf_i1[j+1] + 1
            else:
                val1 = suf_i1[j]
                val2 = suf_i[j+1]
                suf_i[j] = val1 if val1 > val2 else val2
                
    # Reconstruct the optimal path lexicographically
    i, j = 0, 0
    ans = []
    while i < N or j < M:
        R = suf[i][j]
        # Option 0: Match (' ') - Weight 0
        if i < N and j < M and old_file[i] == new_file[j] and suf[i+1][j+1] == R - 1:
            ans.append(' ' + old_file[i])
            i += 1
            j += 1
        # Option 1: Delete ('-') - Weight 1
        elif i < N and suf[i+1][j] == R:
            ans.append('-' + old_file[i])
            i += 1
        # Option 2: Add ('+') - Weight 2
        elif j < M and suf[i][j+1] == R:
            ans.append('+' + new_file[j])
            j += 1
            
    print('\n'.join(ans))

if __name__ == '__main__':
    solve()