# External reference: http://cs101.openjudge.cn/practice/01835/statistics/
# Accepted submission: 51713088
# Source: http://cs101.openjudge.cn/practice/solution/51713088/
# License: not declared on the submission page; no license is inferred.

m = int(input().strip())
for _ in range(m):
    n = int(input().strip())
    face = 0
    top = 2
    left = 4
    x = y = z = 0
    for _ in range(n):
        cmd, dist = input().strip().split()
        dist = int(dist)
        if cmd == "forward":
            d = face
        elif cmd == "back":
            d = (face + 3) % 6
        elif cmd == "left":
            d = left
        elif cmd == "right":
            d = (left + 3) % 6
        elif cmd == "up":
            d = top
        elif cmd == "down":
            d = (top + 3) % 6
        else:
            continue
        if d == 0:
            x += dist
        elif d == 1:
            y += dist
        elif d == 2:
            z += dist
        elif d == 3:
            x -= dist
        elif d == 4:
            y -= dist
        elif d == 5:
            z -= dist
        if cmd == "back":
            face = (face + 3) % 6
            left = (left + 3) % 6
        elif cmd == "left":
            new_face = left
            new_left = (face + 3) % 6
            face, left = new_face, new_left
        elif cmd == "right":
            new_face = (left + 3) % 6
            new_left = face
            face, left = new_face, new_left
        elif cmd == "up":
            new_face = top
            new_top = (face + 3) % 6
            face, top = new_face, new_top
            pass
        elif cmd == "down":
            new_face = (top + 3) % 6
            new_top = face
            face, top = new_face, new_top
            pass
    print(x, y, z, face)
