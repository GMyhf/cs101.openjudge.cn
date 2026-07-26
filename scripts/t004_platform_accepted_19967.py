# External reference: cs101.openjudge.cn practice/19967 statistics, Accepted solution 51312141.
# Source: http://cs101.openjudge.cn/practice/solution/51312141/
# Statistics: http://cs101.openjudge.cn/practice/19967/statistics/
# License: not declared on submission page; no license inferred
N = int(input())
l = []
for _ in range(N):
    inp = input().split()
    if inp[0] == '+':
        idx, data = int(inp[1]), int(inp[2])
        l.insert(idx, data)
    elif inp[0] == '-':
        idx = int(inp[1])
        del l[idx]
    elif inp[0] == '*':
        idx, data = int(inp[1]), int(inp[2])
        l[idx] = data
    elif inp[0] == '?':
        data = int(inp[1])
        if data not in l:
            print('Failed')
        else:
            print(l.index(data))
