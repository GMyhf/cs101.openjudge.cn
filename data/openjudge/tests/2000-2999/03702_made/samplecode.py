import math, sys
def solve(text):
    v = list(map(int, text.split())); n = v[0]; p = [tuple(v[1+3*i:4+3*i]) for i in range(n)]
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            d = math.dist(p[i], p[j]); pairs.append((d, i, j))
    pairs.sort(key=lambda x: -x[0])
    return ''.join(f'({p[i][0]},{p[i][1]},{p[i][2]})-({p[j][0]},{p[j][1]},{p[j][2]})={d:.2f}\n' for d,i,j in pairs)
if __name__ == '__main__': sys.stdout.write(solve(sys.stdin.read()))
