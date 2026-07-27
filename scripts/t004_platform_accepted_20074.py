# External reference: cs101.openjudge.cn practice/20074 statistics, Accepted solution 51318992.
# Source: http://cs101.openjudge.cn/practice/solution/51318992/
# Statistics: http://cs101.openjudge.cn/practice/20074/statistics/
# License: not declared on submission page; no license inferred
n = int(input())
Man, Woman = 0, 0
for _ in range(n):
    h, w, s = input().split()
    min_w = 18.5*(float(h)/100)**2
    max_w = 24.9*(float(h)/100)**2
    cur_w = float(w)
    num = 0
    while cur_w < min_w or cur_w > max_w:
        if cur_w < min_w:
            cur_w += 8
        elif cur_w > max_w:
            cur_w -= 5
        num += 1
    if s == 'M':
        Man = max(Man, num)
    elif s == 'F':
        Woman = max(Woman, num)
print(int(Man), int(Woman))
