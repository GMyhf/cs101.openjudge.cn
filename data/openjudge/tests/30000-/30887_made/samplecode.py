# External reference: http://cs101.openjudge.cn/practice/30887/statistics/
# Accepted submission: 52674601
# Source: http://cs101.openjudge.cn/practice/solution/52674601/
# License: not declared on the submission page; no license is inferred.

def cal(a, target):
    ans = 0
    for x in a:
        d = target - x
        if d <= 0:
            ans += -d
        else:
            if d % 2 == 0:
                ans += d//2
            else:
                ans += (d+3)//2
    return ans
def main():
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    k = (2*n+2) // 3
    q = a[k-1]
    res = min(cal(a, q-1), cal(a, q))
    print(res)
if __name__ == "__main__":
    main()
