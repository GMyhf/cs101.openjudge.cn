a=int(input())
b=list(map(int, input().split()))
b.sort()
c=int(input())
left=0
right=a-1
while left<right:
    while b[left]+b[right]>c:
        right-=1
    if b[left]+b[right]==c:
        print(b[left],b[right],end=" ")
        quit()
    else:
        left+=1
print("No")