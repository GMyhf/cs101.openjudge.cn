a,b,c=map(int,input().split())
result=0
for k in range(c//b+1):
    if (c-b*k)%a==0:
        result+=1
print(result)