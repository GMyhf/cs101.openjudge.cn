#!/usr/bin/env python3
"""986D Perfect Encoding: exact integer arithmetic, never logarithms."""
import sys

try:
    sys.set_int_max_str_digits(2_000_000)
except AttributeError:
    pass


def maximum_product(total):
    if total <= 1:
        return 1
    quotient, remainder = divmod(total, 3)
    if remainder == 0:
        return 3 ** quotient
    if remainder == 1:
        return 4 * 3 ** (quotient - 1)
    return 2 * 3 ** quotient


target = int(sys.stdin.buffer.readline())
low, high = 0, max(3, len(str(target)) * 3)
while low < high:
    middle = (low + high) // 2
    if maximum_product(middle) >= target:
        high = middle
    else:
        low = middle + 1
print(low)
