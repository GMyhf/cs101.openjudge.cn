# External reference: http://cs101.openjudge.cn/practice/01166/statistics/
# Accepted submission: 51696081
# Source: http://cs101.openjudge.cn/practice/solution/51696081/
# License: not declared on the submission page; no license is inferred.

cond = []
for _ in range(3):
    cond += [int(x) for x in input().split()]
move_effect = [[0, 1, 3, 4], [0, 1, 2], [1, 2, 4, 5], [0, 3, 6], [1, 3, 4, 5, 7], [2, 5, 8], [3, 4, 6, 7], [6, 7, 8], [4, 5, 7, 8]]
for num in range(28):
    cnt = [0]*9
    def dfs(k, used):
        if k == 9:
            if used != num:
                return False
            for clock in range(9):
                judge = 0
                for move in range(9):
                    if clock in move_effect[move]:
                        judge += cnt[move]
                if (cond[clock]+judge) % 4 != 0:
                    return False
            return True
        for count in range(4):
            if used + count > num:
                break
            cnt[k] = count
            if dfs(k+1, used+count):
                return True
        return False
    if dfs(0, 0):
        res = []
        for move in range(9):
            res.extend([str(move+1)]*cnt[move])
        print(' '.join(res))
