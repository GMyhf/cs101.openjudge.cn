# External reference: statistics page /practice/23744/
# Accepted submission: 52178544
# Source: http://cs101.openjudge.cn/practice/solution/52178544/
# License: not declared on the submission page; no license is inferred.

# External reference: statistics page /practice/23744/
# Accepted submission: 52178544
# Source: http://cs101.openjudge.cn/practice/solution/52178544/
# License: not declared on the submission page; no license is inferred.

a,b,c=map(float,input().split())
x=min(a,b+c)
y=min(b,a+c)
xy=min(c,a+b)
lis=[]
for i in range(3):
    lis.append(list(input().split()))
    lis[i][1]=int(lis[i][1])
    lis[i][2]=int(lis[i][2])
dir=[(0,1,2),(0,2,1),(1,2,0),(1,0,2),(2,0,1),(2,1,0)]
mi=float("inf")
def path(x1,y1,x2,y2):
    p=abs(x1-x2)
    q=abs(y1-y2)
    zan=min(p,q)
    p-=zan
    q-=zan
    return zan*xy+p*x+q*y
def shi(aa,bb,cc):
    zan=0
    zan+=path(0,0,lis[aa][1],lis[aa][2])
    zan+=path(lis[bb][1],lis[bb][2],lis[aa][1],lis[aa][2])
    zan+=path(lis[cc][1],lis[cc][2],lis[bb][1],lis[bb][2])
    zan+=path(lis[cc][1],lis[cc][2],100,100)
    return zan
ans1,ans2,ans3="a","a","a"
for dx,dy,dz in dir:
    k=shi(dx,dy,dz)
    if (k<mi):
        mi=k
        ans1,ans2,ans3=dx,dy,dz
print(lis[ans1][0],lis[ans2][0],lis[ans3][0])
print(f"{mi:.2f}")