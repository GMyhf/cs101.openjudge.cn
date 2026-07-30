# External reference: http://cs101.openjudge.cn/practice/30571/statistics/
# Accepted submission: 52789487
# Source: http://cs101.openjudge.cn/practice/solution/52789487/
# License: not declared on the submission page; no license is inferred.

class Solution:
    def bitwiseComplement(self, n: int) -> int:
        if n == 0:
            return 1

        # n.bit_length() 返回 n 的二进制有效位数
        mask = (1 << n.bit_length()) - 1
        return mask ^ n  # 或者 return mask - n

if __name__ == "__main__":
    sol = Solution()
    n = int(input())
    print(sol.bitwiseComplement(n))
