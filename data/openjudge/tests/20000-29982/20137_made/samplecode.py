# External reference: statistics page /practice/20137/
# Accepted submission: 32302039
# Source: http://cs101.openjudge.cn/practice/solution/32302039/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/20137 statistics, Accepted solution 32302039.
# Source: http://cs101.openjudge.cn/practice/solution/32302039/
# Statistics: http://cs101.openjudge.cn/practice/20137/statistics/
# License: not declared on submission page; no license inferred
r,c=map(int,input().split())
a,b=map(int,input().split())
d1,d2=map(int,input().split())
flag=[[-1]*(c+3),*[[-1]+[0]*(c+1)+[-1] for _ in range(r+1)],[-1]*(c+3)]
a+=1;b+=1
flag[a][b]=1
cnt=1
while(True):
    a+=d1;b+=d2
    if(flag[a][b]==1 or (flag[a-d1][b]==1 and flag[a][b-d2]==1)):
        break
    if(flag[a][b]==-1):
        if(flag[a-d1][b]==-1 and flag[a][b-d2]==-1):
            break
        elif(a==0 or a==r+2):
            a-=d1
            if(flag[a][b]==1):
                break
            flag[a][b]=1;cnt+=1
            if(flag[a+d1][b]==-1 and flag[a][b+d2]==-1):
                break
            d1=-d1
        else:
            b -= d2
            if (flag[a][b] == 1):
                break
            cnt += 1
            flag[a][b] = 1
            if (flag[a + d1][b] == -1 and flag[a][b + d2] == -1):
                break
            d2=-d2
    else: flag[a][b]=1;cnt+=1
print(cnt)

