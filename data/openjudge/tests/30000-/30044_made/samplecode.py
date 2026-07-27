# External reference: /practice/30044/statistics/
# Accepted submission: 52732985
# Source: http://cs101.openjudge.cn/practice/solution/52732985/
# License: not declared on the submission page; no license is inferred.

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i*i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def reverse_bin(num):
    s = bin(num)[2:]       # 转二进制，去掉0b
    rev = s[::-1]
    return int(rev, 2)

pairs_set = set()
res_list = []
num = 3

while len(res_list) <= 1000:
    if is_prime(num):
        rev_num = reverse_bin(num)
        if is_prime(rev_num):
            a = min(num, rev_num)
            b = max(num, rev_num)
            if (a,b) not in pairs_set:
                pairs_set.add((a,b))
                res_list.append((a,b))
    num += 1

x = int(input())
print(res_list[x][0], res_list[x][1])