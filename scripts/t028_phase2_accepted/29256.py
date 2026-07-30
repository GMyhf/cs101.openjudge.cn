# External reference: http://cs101.openjudge.cn/practice/29256/statistics/
# Accepted submission: 52734185
# Source: http://cs101.openjudge.cn/practice/solution/52734185/
# License: not declared on the submission page; no license is inferred.

def main():
    import sys
    input = sys.stdin.read().split()
    idx = 0
    n = int(input[idx])
    m = int(input[idx+1])
    idx += 2
    a = list(map(int, input[idx:idx+n]))

    # 二分范围
    left = max(a)
    right = sum(a)
    ans = right

    while left <= right:
        mid = (left + right) // 2
        groups = 1
        current = 0

        for num in a:
            if current + num > mid:
                groups += 1
                current = num
            else:
                current += num

        if groups <= m:
            # 可以分，尝试更小
            ans = mid
            right = mid - 1
        else:
            # 不够分，需要更大
            left = mid + 1
    print(ans)

if __name__ == "__main__":
    main()
