# External reference: http://cs101.openjudge.cn/practice/18161/statistics/
# Accepted submission: 51773075
# Source: http://cs101.openjudge.cn/practice/solution/51773075/
# License: not declared on the submission page; no license is inferred.

def matrix_mult(m1,m2):
    r,c=len(m1),len(m2[0])
    rt,ct=len(m2),len(m1[0])
    if rt != ct:
        return 0
    ans=[[0]*c for _ in range(r)]
    for i in range(r):
        for j in range(c):
            for m in range(len(m1[0])):
                ans[i][j]+=m1[i][m]*m2[m][j]
    return ans
def matrix_add(m1,m2):
    r,c=len(m1),len(m1[0])
    rt,ct=len(m2),len(m2[0])
    if r!=rt or c !=ct:
        return 0
    ans=[[0]*c for _ in range(r)]
    for i in range(r):
        for j in range(c):
            ans[i][j]=m1[i][j]+m2[i][j]
    return ans
def main():
    rA,cA=map(int,input().split())
    matrixA=[list(map(int,input().split())) for _ in range(rA)]
    rB,cB=map(int,input().split())
    matrixB=[list(map(int,input().split())) for _ in range(rB)]
    rC,cC=map(int,input().split())
    matrixC=[list(map(int,input().split())) for _ in range(rC)]
    mul=matrix_mult(matrixA,matrixB)
    if not mul:
        print('Error!')
        return
    ans=matrix_add(mul,matrixC)
    if not ans:
        print('Error!')
        return
    for line in ans:
        print(*line)
    return
if __name__ == '__main__':
    main()
