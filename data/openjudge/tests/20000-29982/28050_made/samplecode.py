# Platform-verified local reference: Accepted submission 53014037.
# Source: http://cs101.openjudge.cn/practice/solution/53014037/
# Locally derived after five existing Python3 Accepted submissions timed out on the
# recorded n=9, start=(0,1) no-tour case and no G++ Accepted source was available.
# The square knight graph is bipartite. Odd boards have one extra even-color square,
# so an open Hamilton path must start on that color; 3x3 and 4x4 have no tour.
# License: project-authored for this repository.

n = int(input())
row, column = map(int, input().split())
possible = n >= 5 and (n % 2 == 0 or (row + column) % 2 == 0)
print("success" if possible else "fail")
