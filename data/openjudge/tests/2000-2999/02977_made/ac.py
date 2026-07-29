p, e, i, d = map(int, input().split())
x = d + 1

while True:
    if x % 23 == p % 23 and x % 28 == e % 28 and x % 33 == i % 33:
        print(x - d)
        break
    x += 1
