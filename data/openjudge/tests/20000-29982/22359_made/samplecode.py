# Source: /home/ubuntu/hongfei/2024spring-cs201/2024spring_dsa_problems.md
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def goldbach(n):
    for i in range(2, n):
        if is_prime(i) and is_prime(n - i):
            return i, n - i

n = int(input())
a, b = goldbach(n)
print(a, b)
