# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
m,n = map(int, input().split())
matrix = []
for i in range(m):
    matrix.append(list(map(int, list(input()))))

def check(matrix, i, j, step):
    for x in range(i, i+step+1):
        for y in range(j, j+step+1):
            if matrix[x][y] == 0:
                return False
    return True

cnt = 0
step = 0

while step <= min(m, n):
    for i in range(m-step):
        for j in range(n-step):
            if check(matrix, i, j, step):
                cnt += 1
    step += 1

print(cnt)
