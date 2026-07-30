# External reference: http://cs101.openjudge.cn/practice/29468/statistics/
# Accepted submission: 49217334
# Source: http://cs101.openjudge.cn/practice/solution/49217334/
# License: not declared on the submission page; no license is inferred.

def is_prime(n):
    """判断 n 是否是质数"""
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def next_prime(n):
    """返回大于等于 n 的最小质数"""
    while not is_prime(n):
        n += 1
    return n

def hash_insert(table, size, num):
    """尝试将 num 插入到散列表 table，返回位置或 '-'"""
    h = num % size
    for i in range(size):
        pos = (h + i*i) % size
        if table[pos] is None:
            table[pos] = num
            return str(pos)
        elif table[pos] == num:
            return str(pos)
    return '-'  # 插入失败

def main():
    N = int(input())
    nums = list(map(int, input().split()))
    size = next_prime(N)
    table = [None] * size
    result = []

    for num in nums:
        result.append(hash_insert(table, size, num))

    print(' '.join(result))

if __name__ == "__main__":
    main()
