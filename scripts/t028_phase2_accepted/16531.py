# External reference: http://cs101.openjudge.cn/practice/16531/statistics/
# Accepted submission: 52675256
# Source: http://cs101.openjudge.cn/practice/solution/52675256/
# License: not declared on the submission page; no license is inferred.

M, N = map(int,input().split())
seat = []
for _ in range(M):
    row = list(map(int,input().split()))
    seat.append(row)
total = M * N
students = [None] * total
scores = [0] * total
for i in range(total):
    raw = input()
    if raw.strip() == '':
        students[i] = []
    else:
        students[i] = list(map(int, raw.split()))
        scores[i] = sum(students[i])
same_neighbor = 0
directions = [(-1, 0),(1,0),(0,-1),(0,1)]
for i in range(M):
    for j in range(N):
        cur_id = seat[i][j]
        cur_ans = students[cur_id]
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < M and 0 <= nj < N:
                nei_id = seat[ni][nj]
                nei_ans = students[nei_id]
                if cur_ans == nei_ans:
                    same_neighbor += 1
                    break
freq ={}
for sc in scores:
    freq[sc] = freq.get(sc, 0) + 1
sorted_scores = sorted(freq.keys(), reverse = True)
max_excellent = total * 2 // 5
cum = 0
for sc in sorted_scores:
    if cum + freq[sc] <= max_excellent:
        cum += freq[sc]
    else:
        break
excellent = cum
print(same_neighbor, excellent)
