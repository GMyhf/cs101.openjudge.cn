import sys
content=sys.stdin.read().split()
ptr=0
while ptr<len(content):
    m=int(content[ptr])
    num=content[ptr+1]
    ptr+=2
    #dp[i][j]表示放i个加号，前j+1位数的最小和，dp[i][j]=max(dp[i][j],dp[i-1][j-t]+int(num[j-t:j]))
    dp=[[float('inf')]*len(num) for _ in range(m+1)]
    for j in range(len(num)):
        dp[0][j]=int(num[:j+1])
    for i in range(1,m+1):
        for j in range(len(num)):
            for t in range(1,j-i+2):
                dp[i][j]=min(dp[i][j],dp[i-1][j-t]+int(num[j-t+1:j+1]))
    print(dp[m][len(num)-1])