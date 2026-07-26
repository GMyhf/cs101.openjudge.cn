n=int(input())
intervals=[]
for i in range(n):
    intervals.append(tuple(int(i) for i in input().split()))
intervals.sort()
cleft=intervals[0][0]
cright=intervals[0][1]
for left,right in intervals:
    if left>cright:
        print("no")
        break
    else:
        cright=max(right,cright)
else:
    print(cleft,cright)