# External reference: /practice/29739/statistics/
# Accepted submission: 52298393
# Source: http://cs101.openjudge.cn/practice/solution/52298393/
# License: not declared on the submission page; no license is inferred.

S=input()
T=input()
n=len(T)
pos1=0
allzero=False
while T[pos1]=='0':
    pos1+=1
    if pos1>=n:
        allzero=True
        break
if allzero:
    for i in 'abcdefghijklmnopqrstuvwxyz':
        if i not in S:
            print(i)
            exit()
    else:
        print('a'*(n+1))
        exit()
target=S[pos1:]+'#'+S
n=len(target)
Z=[0]*n
Z[0]=n
left=0
right=0
for i in range(1,n):
    if i>right: #那么开始暴力匹配
        ptr=0
        while ptr<n-i and target[ptr]==target[ptr+i]:
            ptr+=1
        Z[i]=ptr #暴力匹配好了，更新Z[i]
        if ptr>0: #如果有效，那么更新安全区
            left=i
            right=i+ptr-1
    elif i<=right: #看来我们有经验，无需暴力匹配
        tmp=Z[i-left]
        if i+tmp<right:
            Z[i]=tmp
        else: #于是，从i出发，到right截止的所有内容全部完成匹配，相当于Z[i]至少是right-i+1.于是我们要从S[right-i+1]开始比较起
            ptr=right
            while ptr<n and target[ptr]==target[ptr-i]:
                ptr+=1
            Z[i]=ptr-i
            if ptr>i:
                left=i
                right=ptr-1
maxlen=float('inf')
minlen=0
nn=len(T)
for i,char in enumerate(T):
    if char=='0':
        minlen=max(minlen,Z[i+(nn-pos1)+1])
    elif char=='1':
        maxlen=min(maxlen,Z[i+(nn-pos1)+1])
if minlen>=maxlen:
    print(-1)
else:
    print(S[pos1:pos1+minlen+1])




