# Codeforces 986D Perfect Encoding -- reference solution.
# Written for this repo as a hand-off artifact (test-data reference); no external license.
#
# For a fixed cost c the largest product of positive parts summing to c uses only 3s,
# plus at most two 2s (a 4 counts as 2+2).  So the answer is
#   min over b in {0,1,2} of 2b + 3k, k = least k >= 0 with 2^b * 3^k >= n,
# and 1 for n = 1 (m >= 1 forces cost >= 1).
# n has up to 1.5e6 digits: the decimal module (libmpdec, NTT multiplication) keeps
# the big-number work exact and fast.
import decimal
import math
import sys


def main():
    s = sys.stdin.readline().strip()
    if s == "1":
        print(1)
        return
    ctx = decimal.Context(prec=len(s) + 30, Emax=decimal.MAX_EMAX, Emin=decimal.MIN_EMIN,
                          traps=[decimal.Inexact, decimal.Rounded, decimal.InvalidOperation])
    decimal.setcontext(ctx)
    n = decimal.Decimal(s)
    head = s[:18]
    log10n = math.log10(int(head)) + (len(s) - len(head))
    k0 = max(0, int(log10n / math.log10(3)) - 3)
    base = decimal.Decimal(3) ** k0
    best = None
    for b in range(3):
        t = base * (1 << b)
        k = k0
        while t < n:
            t *= 3
            k += 1
        cost = 2 * b + 3 * k
        if best is None or cost < best:
            best = cost
    print(best)


main()
