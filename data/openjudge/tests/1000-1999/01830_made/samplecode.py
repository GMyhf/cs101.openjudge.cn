import sys

IMPOSSIBLE = "Oh,it's impossible~!!"

def one_case(n, start, target, edges):
    rows = []
    for j in range(n):
        mask = 0
        for i, k in edges:
            if k == j: mask ^= 1 << i
        rows.append(mask | (((start[j] ^ target[j]) & 1) << n))
    rank = 0
    for col in range(n):
        pivot = next((r for r in range(rank, n) if (rows[r] >> col) & 1), None)
        if pivot is None: continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(n):
            if r != rank and ((rows[r] >> col) & 1): rows[r] ^= rows[rank]
        rank += 1
    if any((row & ((1 << n) - 1)) == 0 and ((row >> n) & 1) for row in rows): return IMPOSSIBLE
    return str(1 << (n - rank))

def solve(text):
    it = iter(text.split())
    k = int(next(it)); answers = []
    for _ in range(k):
        n = int(next(it))
        if n == 0: break
        start = [int(next(it)) for _ in range(n)]; target = [int(next(it)) for _ in range(n)]
        edges = []
        while True:
            i, j = int(next(it)), int(next(it))
            if i == j == 0: break
            edges.append((i - 1, j - 1))
        answers.append(one_case(n, start, target, edges))
    return '\n'.join(answers) + ('\n' if answers else '')

if __name__ == '__main__': sys.stdout.write(solve(sys.stdin.read()))
