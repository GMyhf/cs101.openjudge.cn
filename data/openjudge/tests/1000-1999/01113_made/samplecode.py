# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1113: Wall
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01113/
# License: not declared; no license is inferred.
import math
N,L=map(int,input().split())
points=[]
for _ in range(N):
    points.append(tuple(map(int,input().split())))
def cross(o,a,b):
	# 矢量叉乘
    return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
def distance(a,b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
# 对x坐标进行排序
points.sort()
# 下凸边
lower=[]
for p in points:
    while len(lower)>1 and cross(lower[-2],lower[-1],p)<=0:
        lower.pop()
    lower.append(p)
# 上凸边
upper=[]
for p in reversed(points):
    while len(upper)>1 and cross(upper[-2],upper[-1],p)<=0:
        upper.pop()
    upper.append(p)
hull=lower[:-1]+upper[:-1]
n=len(hull)
l=0
for i in range(n):
    j=(i+1)%n
    l+=distance(hull[i],hull[j])
l+=2*math.pi*L
print(f'{l:.0f}')
