# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
n = int(input())
step = [[1, 0], [-1, 0], [0, 1]]
num = 1


def dfs(x, y, m, visited):
    global num
    if m == 0:
        return
    visited.append([x, y])
    num -= 1
    for j in range(3):
        if [x+step[j][0], y+step[j][1]] not in visited:
            num += 1
            lista = []
            lista += visited
            dfs(x+step[j][0], y+step[j][1], m-1, lista)


dfs(0, 0, n, [])
print(num)
