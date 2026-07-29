# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 3247: 回文素数
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/03247/
# License: not declared; no license is inferred.
import sys
import math

def is_prime(num):
    if num < 2:
        return False
    if num in {2, 3, 5, 7}:
        return True
    if num % 2 == 0 or num % 5 == 0:
        return False
    for i in range(3, int(math.sqrt(num)) + 1, 2):
        if num % i == 0:
            return False
    return True

def generate_palindromes(n):
    palindromes = []
    if n == 1:
        return [2, 3, 5, 7]  # 1位数的素数回文数

    half_len = (n + 1) // 2  # 只需要构造前半部分
    start, end = 10**(half_len - 1), 10**half_len

    for first_half in range(start, end):
        first_half_str = str(first_half)
        if n % 2 == 0:  # 偶数位
            palindrome = int(first_half_str + first_half_str[::-1])
        else:  # 奇数位
            #palindrome = int(first_half_str + first_half_str[-2::-1])
            palindrome = int(first_half_str + first_half_str[:-1][::-1])

        if is_prime(palindrome):
            palindromes.append(palindrome)

    return palindromes

def find_palindromic_primes(n):
    primes = generate_palindromes(n)
    print(len(primes))
    print(" ".join(map(str, primes)))

# 输入
n = int(input().strip())
find_palindromic_primes(n)
