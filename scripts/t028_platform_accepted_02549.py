# External reference: http://cs101.openjudge.cn/practice/02549/statistics/
# Accepted submission: 51482198
# Source: http://cs101.openjudge.cn/practice/solution/51482198/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    input_data = sys.stdin.read().strip().split()
    idx = 0
    results = []

    while True:
        n = int(input_data[idx]); idx += 1
        if n == 0:
            break

        S = []
        for _ in range(n):
            S.append(int(input_data[idx])); idx += 1

        S.sort()
        found = False
        ans = None

        # 从大到小枚举d（作为答案）
        for d_idx in range(n-1, -1, -1):
            d = S[d_idx]
            if found:
                break

            # 枚举c（作为减数）
            for c_idx in range(n):
                if c_idx == d_idx:
                    continue
                c = S[c_idx]
                target = d - c

                # 使用哈希表来寻找a+b=target
                seen = set()
                for a_idx in range(n):
                    if a_idx == d_idx or a_idx == c_idx:
                        continue
                    a = S[a_idx]
                    b = target - a

                    # 检查b是否在集合中，并且b不是a,c,d
                    if b in seen:
                        # 还需要检查b是否在S中，并且b不是a,c,d
                        # 由于S是排序的，我们可以用二分查找检查b是否存在
                        # 但更简单的是：b已经在seen中，说明b是S中的某个元素
                        # 我们只需要确保b不是a,c,d
                        if (b != a and b != c and b != d and
                            a != c and a != d):
                            # 还需要确认b确实是S中的元素（不是巧合的数字）
                            # 由于seen是从S中添加的，所以b一定是S中的元素
                            ans = d
                            found = True
                            break
                    seen.add(a)

                if found:
                    break

        if found:
            results.append(str(ans))
        else:
            results.append("no solution")

    print("\n".join(results))

if __name__ == "__main__":
    solve()
