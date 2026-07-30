# External reference: http://cs101.openjudge.cn/practice/18155/statistics/
# Accepted submission: 51275594
# Source: http://cs101.openjudge.cn/practice/solution/51275594/
# License: not declared on the submission page; no license is inferred.

T = int(input())
S = [int(x) for x in input().split()]
def dfs(S, T, cur_state, is_null, cur_pos):
    if is_null == False and cur_state == T:
        return True
    if cur_pos == len(S):
        return False
    if dfs(S, T, cur_state*S[cur_pos], False, cur_pos+1):
        return True
    if dfs(S, T, cur_state, is_null, cur_pos+1):
        return True
    return False
if dfs(S, T, 1, True, 0):
    print('YES')
else:
    print('NO')
