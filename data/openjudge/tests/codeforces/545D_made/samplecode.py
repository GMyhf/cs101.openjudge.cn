#!/usr/bin/env python3
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    t = [int(data[i + 1]) for i in range(n)]
    t.sort()

    count = 0
    prefix_sum = 0
    for i in range(n):
        if prefix_sum <= t[i]:
            count += 1
            prefix_sum += t[i]
        # else: this customer is disappointed, but we still serve them
        # Actually, we want to maximize satisfied customers
        # If a customer is not satisfied, we don't need to include them
        # Wait - re-read problem. We arrange queue order. A customer is satisfied
        # if the sum of service times of all people before them <= their own service time.
        # We want to maximize number of satisfied customers.
        # Greedy: sort ascending. For each, if satisfied, count them and add their time.
        # If not satisfied, skip them (don't put them in queue before satisfied ones).
        # Actually, skipping is better since they'd add to the prefix without being satisfied.

    # Let me redo this properly
    count = 0
    prefix_sum = 0
    for i in range(n):
        if prefix_sum <= t[i]:
            count += 1
            prefix_sum += t[i]
    print(count)

solve()
