# Written for this repository from the public problem statement; no external submission used.
import sys


lines = sys.stdin.read().splitlines()
mode = int(lines[0])

if mode == 1:
    print(abs(int(lines[1])))
elif mode in (2, 3):
    a, b, c = map(int, lines[1].split())
    values = (a + b, b + c, a + c)
    print(*values, sep=" " if mode == 2 else "\n")
elif mode == 4:
    print(*lines[1].split(), sep="->")
elif mode == 5:
    print(*(value + "#" for value in lines[2].split()), sep="")
elif mode == 6:
    print(*sorted(map(int, lines[2].split()), reverse=True))
elif mode == 7:
    a, b = map(int, lines[1].split())
    print(f"{a}*{b}={a * b}")
elif mode == 8:
    a, b = map(int, lines[1].split())
    print(f"{a / b:.3f}")
elif mode == 9:
    print(*lines[2].split(), sep=",")
