# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 1941: The Sierpinski Fractal
# Fenced code block index: 3
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01941/
# License: not declared; no license is inferred.
import sys
def f(n):
    if n == 1:
        return [' /\\ ', '/__\\']
    t = f(n - 1)
    x = 2 ** (n - 1)
    res = [' ' * x + u + ' ' * x for u in t]
    res.extend([u + u for u in t])
    return res


al = [f(i) for i in range(1, 11)]
while True:
    n = int(input())
    if n == 0:
        break
    for u in al[n - 1]:
        print(u)
    print()
