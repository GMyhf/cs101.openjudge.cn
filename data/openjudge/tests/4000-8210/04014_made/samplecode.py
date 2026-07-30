# External reference: http://cs101.openjudge.cn/practice/04014/statistics/
# Accepted submission: 50765156
# Source: http://cs101.openjudge.cn/practice/solution/50765156/
# License: not declared on the submission page; no license is inferred.

while True:
    try:
        x = input().split()
        str_ = x[0]
        num = int(x[1])
        sequence = x[2:]
        res = ''
        for i in str_:
            res += chr((ord(i)-65+num)%26+65)
        ans = ''
        for i in sequence:
            ans += res[int(i)-1]
        print(ans)
    except EOFError:
        break
