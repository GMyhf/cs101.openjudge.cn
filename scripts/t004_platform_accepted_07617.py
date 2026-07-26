n = int(input())
l = [int(x) for x in input().split()]
k = int(input())
l.sort()
for i in range(-1, -k-1, -1):
    print(l[i])