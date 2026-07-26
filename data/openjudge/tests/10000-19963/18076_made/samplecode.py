# External reference: statistics page /practice/18076/
# Accepted submission: 17302978
# Source: http://cs101.openjudge.cn/practice/solution/17302978/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/18076 statistics, Accepted solution 17302978.
# Source: http://cs101.openjudge.cn/practice/solution/17302978/
# Statistics: http://cs101.openjudge.cn/practice/18076/statistics/
# License: not declared on submission page; no license inferred
a, b = map(int, input().split())
GA_bond = {}
for i in range(a):
    temp = list(map(int, input().split()))
    GA_bond[temp[0]] = GA_bond.get(temp[0], [[]]) + temp[-2:-1]
    root = GA_bond.get(temp[1], [[]])
    root[0].append([temp[0], temp[-1]])
    GA_bond[temp[1]] = root
GB_bond = {}
for i in range(b):
    temp = list(map(int, input().split()))
    GB_bond[temp[0]] = GB_bond.get(temp[0], [[]]) + temp[-2:-1]
    root = GB_bond.get(temp[1], [[]])
    root[0].append([temp[0], temp[-1]])
    GB_bond[temp[1]] = root
G = [GA_bond, GB_bond]

def get_connect(g, m):
    connect = []
    for i in g[0]:
        for j in range(i[1]):
            connect.append(G[m][i[0]][1])
    return connect

def compare(a, b):
    if a>b:
        return 1
    if a<b:
        return 2
    return 0

def get_next_index(connect):
    connect.append(-2)
    same = 0
    while True:
        if connect[same]!=connect[same+1]:
            break
        same += 1
    ma = 0
    for i in range(same):
        if main(connect[ma], connect[i+1])==2:
            ma = i+1
    return connect[ma]

def main(ia=0, ib=0):
    i = 0
    while i<1000000:
        ga = GA_bond[ia]
        gb = GB_bond[ib]
        if compare(ga[1], gb[1]): return compare(ga[1], gb[1])
        connect_a = get_connect(ga, 0)
        connect_b = get_connect(gb, 1)
        connect_a.sort(reverse=True)
        connect_b.sort(reverse=True)
        for i in range(min(len(connect_a), len(connect_b))):
            if compare(connect_a[i], connect_b[i]): return compare(connect_a[i], connect_b[i])
        ia = get_next_index(connect_a)
        ib = get_next_index(connect_b)
        i += 1

print(main())
