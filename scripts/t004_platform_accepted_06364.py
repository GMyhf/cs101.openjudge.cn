n, k = map(int, input().split())

round1 = []
for i in range(n):
    a, b = map(int, input().split())
    round1.append((a, b, i+1))

round1.sort(key = lambda x : -x[0])

round2 = round1[:k]

round2.sort(key = lambda x : -x[1])

print(round2[0][2])