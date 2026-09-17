#!/usr/bin/env python3
# Reference solution for Codeforces 1970E2 "Trails (Medium)".
# Written for this repository as a hand-off artifact for judge-data generation;
# no external source, no external license.
#
# One day from cabin i to cabin j has s_i*s_j + s_i*l_j + l_i*s_j = t_i*t_j - l_i*l_j
# trail pairs (t = s + l), so the transfer matrix is t t^T - l l^T (rank <= 2).
# After day 1 the row vector is t_1*t - l_1*l; it stays in span{t, l}, and one more
# day maps coefficients (a, b) -> (a*TT + b*TL, -(a*TL + b*LL)).  Power the 2x2 map.
import sys

MOD = 1_000_000_007


def mat_mul(x, y):
    return [[(x[0][0] * y[0][0] + x[0][1] * y[1][0]) % MOD, (x[0][0] * y[0][1] + x[0][1] * y[1][1]) % MOD],
            [(x[1][0] * y[0][0] + x[1][1] * y[1][0]) % MOD, (x[1][0] * y[0][1] + x[1][1] * y[1][1]) % MOD]]


def main():
    data = sys.stdin.buffer.read().split()
    m, n = int(data[0]), int(data[1])
    s = list(map(int, data[2:2 + m]))
    l = list(map(int, data[2 + m:2 + 2 * m]))
    t = [a + b for a, b in zip(s, l)]
    tt = sum(x * x for x in t) % MOD
    tl = sum(x * y for x, y in zip(t, l)) % MOD
    ll = sum(y * y for y in l) % MOD
    # column-vector form: (a, b)^T <- A (a, b)^T, A = [[TT, TL], [-TL, -LL]]
    step = [[tt, tl], [(-tl) % MOD, (-ll) % MOD]]
    power = [[1, 0], [0, 1]]
    e = n - 1
    while e:
        if e & 1:
            power = mat_mul(power, step)
        step = mat_mul(step, step)
        e >>= 1
    a0, b0 = t[0] % MOD, (-l[0]) % MOD
    a = (power[0][0] * a0 + power[0][1] * b0) % MOD
    b = (power[1][0] * a0 + power[1][1] * b0) % MOD
    print((a * (sum(t) % MOD) + b * (sum(l) % MOD)) % MOD)


main()
