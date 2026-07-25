# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import sys

def solve():
    data = sys.stdin.read().split()
    if not data: return
    it = iter(data)
    n, k = int(next(it)), int(next(it))
    
    counts = {}
    last_owner = {}
    for p_idx in range(n):
        for _ in range(k):
            val = int(next(it))
            counts[val] = counts.get(val, 0) + 1
            last_owner[val] = p_idx # 覆盖更新，由于 p_idx 递增，最后存的是最大编号

    prob_weights = [0] * n
    for val, c in counts.items():
        prob_weights[last_owner[val]] += c
        
    total = n * k
    for w in prob_weights:
        print(f"{w/total:.9f}")

solve()
