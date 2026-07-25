# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
#蒋子轩
def dfs(rem_sticks,rem_len,target):
    if rem_sticks==0 and rem_len==0:
        return True
    if rem_len==0:
        rem_len=target
    for i in range(n):
        if not used[i] and lens[i]<=rem_len:
            used[i]=True
            if dfs(rem_sticks-1,rem_len-lens[i],target):
                return True
            else:
                used[i]=False
                if lens[i]==rem_len or rem_len==target:
                    return False
    return False
while True:
    n=int(input())
    if n==0:
        break
    lens=list(map(int,input().split()))
    lens.sort(reverse=True)
    total_len=sum(lens)
    for l in range(lens[0],total_len//2+1):
        if total_len%l!=0:
            continue
        used=[False]*n
        if dfs(n,l,l):
            print(l)
            break
    else:
        print(total_len)
