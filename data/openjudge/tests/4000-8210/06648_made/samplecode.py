# External reference: statistics page /practice/06648/
# Accepted submission: 52710633
# Source: http://cs101.openjudge.cn/practice/solution/52710633/
# License: not declared on the submission page; no license is inferred.

import sys
import heapq
def solve():
    input_data = sys.stdin.read().strip().split()
    t = int(input_data[0])
    idx = 1
    results = []
    for _ in range(t):
        m = int(input_data[idx])
        idx += 1
        n = int(input_data[idx])
        idx += 1
        sequences = []
        for _ in range(m):
            seq = []
            for _ in range(n):
                seq.append(int(input_data[idx]))
                idx += 1
            seq.sort()
            sequences.append(seq)
        candidates = sequences[0][:]
        for i in range(1, m):
            current_seq = sequences[i]
            heap = []
            for val in candidates:
                heapq.heappush(heap, (val + current_seq[0], 0))
            new_candidates = []
            for _ in range(n):
                if not heap:
                    break
                current_sum, pos = heapq.heappop(heap)
                new_candidates.append(current_sum)
                if pos + 1 < n:
                    next_sum = current_sum - current_seq[pos] + current_seq[pos + 1]
                    heapq.heappush(heap, (next_sum, pos + 1))
            candidates = new_candidates
        results.append(" ".join(map(str, candidates)))
    return "\n".join(results)
if __name__ == "__main__":
    print(solve())