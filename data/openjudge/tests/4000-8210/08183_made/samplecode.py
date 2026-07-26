# External reference: statistics page /practice/08183/
# Accepted submission: 51158010
# Source: http://cs101.openjudge.cn/practice/solution/51158010/
# License: not declared on the submission page; no license is inferred.

a, b, c, d = input().split()
height, width = int(a), int(b)
kind_1 = [c]*width
kind_2 = [c]+[' ']*(width-2)+[c]
if d == '0':
    print(*kind_1, sep = '')
    for _ in range(height-2):
        print(*kind_2, sep = '')
    print(*kind_1, sep = '')
elif d == '1':
    for _ in range(height):
        print(*kind_1, sep = '')