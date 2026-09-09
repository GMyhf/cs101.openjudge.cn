# Written for this repository from the public problem statement; no external submission used.
import sys


lines = sys.stdin.read().splitlines()
mode = int(lines[0])

if mode == 1:
    print(lines[1])
elif mode == 2:
    x = int(lines[1])
    print(x * x)
elif mode == 3:
    a, b, c = lines[1].split()
    print(c, b, a)
elif mode == 4:
    a, b = map(int, lines[1].split())
    print(a + b, a * b)
elif mode == 5:
    values = list(map(int, lines[1].split()))
    print(len(values), sum(values), max(values))
elif mode == 6:
    print(sum(map(int, lines[1:-1])))
elif mode == 7:
    n = int(lines[1])
    print(*(sum(map(int, line.split())) for line in lines[2:2 + n]))
elif mode == 8:
    a, b, c = lines[1].split(",")
    print(c, b, a)
