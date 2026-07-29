# External reference: http://cs101.openjudge.cn/practice/02286/statistics/
# Accepted submission: 44694931
# Source: http://cs101.openjudge.cn/practice/solution/44694931/
# License: not declared on the submission page; no license is inferred.

line = {'A': [0, 2, 6, 11, 15, 20, 22],
        'B': [1, 3, 8, 12, 17, 21, 23],
        'C': [10, 9, 8, 7, 6, 5, 4],
        'D': [19, 18, 17, 16, 15, 14, 13],
        'E': [23, 21, 17, 12, 8, 3, 1],
        'F': [22, 20, 15, 11, 6, 2, 0],
        'G': [13, 14, 15, 16, 17, 18, 19],
        'H': [4, 5, 6, 7, 8, 9, 10]
        }
center = [6, 7, 8, 11, 12, 15, 16, 17]

def check():
    for i in range(8):
        if mp[center[i]] != mp[center[0]]:
            return False
    return True

def move(r):
    tmp = [mp[line[r][i]] for i in range(7)]
    for j in range(7):
        mp[line[r][j-1]] = tmp[j]

def move_back(c):
    tmp = [mp[line[c][i]] for i in range(7)]
    for j in range(-1, 6):
        mp[line[c][j+1]] = tmp[j]

def diff(t):
    cnt = 0
    for i in range(8):
        if mp[center[i]] != t:
            cnt += 1
    return cnt

def h():
    return min(diff(1), diff(2), diff(3))

def dfs(dep, max_d):
    if check():
        print(''.join(ans))
        return True
    if dep+h() > max_d:
        return False
    for letter in 'ABCDEFGH':
        ans.append(letter)
        move(letter)
        if dfs(dep+1, max_d):
            return True
        ans.pop()
        move_back(letter)
    return False

while True:
    mp = list(map(int, input().split()))
    if mp == [0]:
        break
    ans = []
    if check():
        print('No moves needed')
    else:
        limit = 1
        while True:
            if dfs(0, limit):
                break
            limit += 1
    print(mp[6])
