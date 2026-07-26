# External reference: cs101.openjudge.cn practice/19164 statistics, Accepted solution 51285327.
# Source: http://cs101.openjudge.cn/practice/solution/51285327/
# Statistics: http://cs101.openjudge.cn/practice/19164/statistics/
# License: not declared on submission page; no license inferred
T, M = map(int, input().split())
p = []
n = []
for _ in range(T):
    P, N = map(int, input().split())
    p.append(P)
    n.append(N)
now_p, now_n = p[0], n[0]
for i in range(1, T):
    last_p, last_n = now_p, now_n
    now_p = max(last_p+p[i], last_n+p[i]-M)
    now_n = max(last_n+n[i], last_p+n[i]-M)
print(max(now_p, now_n))
