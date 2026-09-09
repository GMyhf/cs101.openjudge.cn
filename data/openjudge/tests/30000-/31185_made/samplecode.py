# Written for this repository from the public problem statement; no external submission used.
import sys


lines = sys.stdin.read().splitlines()
mode, rule = map(int, lines[0].split())
n = int(lines[1])

if mode in (1, 5):
    values = list(map(int, lines[2].split()))
    original = values[:]
    values.sort(reverse=rule == 2)
    if mode == 5:
        print(*original)
    print(*values)
    if mode == 1:
        print(max(values), min(values))
elif mode == 2:
    values = lines[2].split()
    values.sort(reverse=rule == 2)
    print(*values)
elif mode in (3, 4, 6):
    width = 3 if mode == 4 else 2
    values = [tuple(map(int, line.split())) for line in lines[2:2 + n]]
    if mode == 3:
        values.sort(key=lambda value: sum(value), reverse=rule == 2)
    elif mode == 4:
        values.sort(key=lambda value: value[1], reverse=rule == 2)
    elif rule == 1:
        values.sort(key=lambda value: value[1], reverse=True)
        values.sort(key=lambda value: value[0])
    else:
        values.sort(key=lambda value: value[1])
        values.sort(key=lambda value: value[0], reverse=True)
    for value in values:
        print(*value[:width])
