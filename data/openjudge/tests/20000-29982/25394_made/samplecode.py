# External reference: statistics page /practice/25394/
# Accepted submission: 52740076
# Source: http://cs101.openjudge.cn/practice/solution/52740076/
# License: not declared on the submission page; no license is inferred.

def solve():
    import sys
    input = sys.stdin.read().split()
    ptr = 0
    k = int(input[ptr])
    ptr += 1
    for _ in range(k):
        n = int(input[ptr])
        ptr += 1
        arr = list(map(int, input[ptr:ptr+n]))
        ptr += n
        max_get = 0
        # 枚举A子集mask1，B子集mask2，无交集
        for mask1 in range(1, 1 << n):
            s1 = 0
            cnt1 = 0
            for i in range(n):
                if mask1 & (1 << i):
                    s1 += arr[i]
                    cnt1 += 1
            if cnt1 == 0:
                continue
            for mask2 in range(1, 1 << n):
                if mask1 & mask2 != 0:  # 元素不能重叠
                    continue
                s2 = 0
                cnt2 = 0
                for i in range(n):
                    if mask2 & (1 << i):
                        s2 += arr[i]
                        cnt2 += 1
                if s1 == s2:
                    if cnt1 + cnt2 > max_get:
                        max_get = cnt1 + cnt2
        print(max_get)

solve()