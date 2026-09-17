#!/usr/bin/env python3
"""02793 孙子问题 —— 参考实现（仓库交接件，非平台提交，不套用外部许可）。

要求 f(N) = Σ b_i·(N mod a_i) 对任意 N 都满足 f(N) ≡ N (mod a_j)，即 f(N) ≡ N (mod L)，
L = lcm(a_1..a_n)。模数不必两两互素，但解总是存在：

把 L 分解成素数幂 q^e。对每个 q^e 取**第一个**满足 q^e | a_i 的下标 i（L 里 q 的次数
就是某个 a_i 里 q 的次数，所以一定有），记 P_i 为分给下标 i 的素数幂之积。取

    b_i ≡ 1 (mod P_i),  b_i ≡ 0 (mod L / P_i)

则 f(N) ≡ N mod a_i ≡ N (mod q^e) 对每个 q^e 成立，于是 f(N) ≡ N (mod L)。b_i 取
[1, L] 里的代表元（≡0 时取 L），L <= lcm(1..50) < 10^22，远不到 50 位。所以本题
**永远不输出 NO**。题面样例 3 5 7 恰好得到 70 21 15。
"""
import sys


def prime_powers(value):
    out, p = [], 2
    while p * p <= value:
        if value % p == 0:
            q = 1
            while value % p == 0:
                value //= p; q *= p
            out.append((p, q))
        p += 1
    if value > 1:
        out.append((value, value))
    return out


def solve(a):
    L = 1
    for x in a:
        L = L * x // gcd(L, x)
    share = [1] * len(a)
    for _, q in prime_powers(L):
        share[next(i for i, x in enumerate(a) if x % q == 0)] *= q
    b = []
    for P in share:
        rest = L // P
        value = rest * pow(rest, -1, P) % L if P > 1 else 0
        b.append(value or L)
    return b


def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def main():
    tokens = sys.stdin.read().split()
    p, out = 0, []
    while p < len(tokens):
        n = int(tokens[p]); p += 1
        if n == 0:
            break
        a = list(map(int, tokens[p:p + n])); p += n
        out.append(" ".join(map(str, solve(a))))
    sys.stdout.write("".join(line + "\n" for line in out))


if __name__ == "__main__":
    main()
