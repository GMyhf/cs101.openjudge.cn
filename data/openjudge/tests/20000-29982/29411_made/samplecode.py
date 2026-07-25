# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
class Solution:
    def intToRoman(self, num: int) -> str:
        roman_numerals = [
            (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
            (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
            (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
        ]

        result = []
        for value, symbol in roman_numerals:
            while num >= value:
                result.append(symbol)
                num -= value
            if num == 0:
                break

        return ''.join(result)

if __name__ == "__main__":
    sol = Solution()
    n = int(input())
    print(sol.intToRoman(n))
