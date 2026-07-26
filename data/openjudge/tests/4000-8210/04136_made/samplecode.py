# External reference: statistics page /practice/04136/
# Accepted submission: 52527332
# Source: http://cs101.openjudge.cn/practice/solution/52527332/
# License: not declared on the submission page; no license is inferred.

r=int(input())
n=int(input())
rects=[]
area=0
for _ in range(n):
    l,t,w,h=[int(i) for i in input().split()]
    rects.append((l,l+w,h))
    area+=w*h
left=0
right=r
while True:
    if right-left<=1:
        ans=right
        break
    mid=left+(right-left)//2
    half=0
    for le,ri,we in rects:
        if ri<=mid:
            half+=(ri-le)*we
        elif ri>mid and le<mid:
            half+=(mid-le)*we
    if half*2>=area:
        right=mid
    else:
        left=mid
left=ans
right=r+1
while True:

    if right-left<=1:
        fans=left
        break
    mid=left+(right-left)//2
    ahalf=0
    for le,ri,we in rects:
        if ri<=ans:
            pass
        elif ri<=mid:
            ahalf+=(ri-le)*we
        elif ri>mid and le<mid:
            ahalf+=(mid-le)*we
    if ahalf==0:
        left=mid
    else:
        right=mid
    
print(fans)