# External reference: cs101.openjudge.cn practice/15291 statistics, Accepted solution 45990573.
# Source: http://cs101.openjudge.cn/practice/solution/45990573/
# Statistics: http://cs101.openjudge.cn/practice/15291/statistics/
# License: not declared on submission page; no license inferred
# print(猫猫)
a, b, c = map(int, input().split())
while a:
    z = 0;
    d = [list(map(int, input().split())) for i in range(a)];
    e = [list(map(int, input().split())) for i in range(b)];
    f = [list(map(int, input().split())) for i in range(c)];

    # 归一化坐标。即减去各自的最小坐标值，使得每个形状的左下角位于 (0, 0)。
    g, h, k, l, o, p = min(i[0] for i in d), min(i[1] for i in d), min(i[0] for i in e), min(i[1] for i in e), min(
        i[0] for i in f), min(i[1] for i in f);
    i, j, m, n, q, r = max(i[0] for i in d) - g, max(i[1] for i in d) - h, max(i[0] for i in e) - k, max(
        i[1] for i in e) - l, max(i[0] for i in f) - o, max(i[1] for i in f) - p;

    # 计算每个形状的边界，用于后续的移动范围确定。
    for y in range(a): d[y][0] -= g;d[y][1] -= h
    for y in range(b): e[y][0] -= k;e[y][1] -= l
    for y in range(c): f[y][0] -= o;f[y][1] -= p

    # 初始化冲突矩阵。用于记录冲突情况和搜索路径。
    s = [20 * [1] for i in range(20)];
    t = [20 * [1] for i in range(20)];
    u = [20 * [1] for i in range(20)];
    v = [[[20 * [0] for i in range(20)] for i in range(20)] for i in range(20)];
    w = [[k - g, l - h, o - g, p - h]];
    x = []

    # 计算冲突矩阵。计算形状 d 和形状 e 在各种相对位置下的冲突情况。
    for a in range(-m, i + 1):
        for b in range(-n, j + 1):
            c = 1
            for g in d:
                for h in e:
                    if g == [h[0] + a, h[1] + b]: c = 0;break
                if c == 0: break
            s[a][b] = c

    # 类似地，计算其他两个冲突矩阵 t 和 u。
    for a in range(-q, i + 1):
        for b in range(-r, j + 1):
            c = 1
            for g in d:
                for h in f:
                    if g == [h[0] + a, h[1] + b]: c = 0;break
                if c == 0: break
            t[a][b] = c
    for a in range(-q, m + 1):
        for b in range(-r, n + 1):
            c = 1
            for g in e:
                for h in f:
                    if g == [h[0] + a, h[1] + b]: c = 0;break
                if c == 0: break
            u[a][b] = c

    # 广度优先搜索。如果找到了一个满足条件的状态，则输出步骤数 z；否则，如果 z 不为零，则输出 -1 表示没有找到解决方案。
    while w:
        for a in w:
            if v[a[0]][a[1]][a[2]][a[3]]: continue
            v[a[0]][a[1]][a[2]][a[3]] = 1
            if (i < a[0] or -m > a[0] or j < a[1] or -n > a[1]) * (i < a[2] or -q > a[2] or j < a[3] or -r > a[3]) * (
                    m < a[2] - a[0] or -q > a[2] - a[0] or n < a[3] - a[1] or -r > a[3] - a[1]): print(
                z);z = -1;x = [];break
            if a[0] <= 10 >= a[2]:
                if s[a[0] + 1][a[1]] * t[a[2] + 1][a[3]]: x.append([a[0] + 1, a[1], a[2] + 1, a[3]])
            if -11 < a[0] and -11 < a[2]:
                if s[a[0] - 1][a[1]] * t[a[2] - 1][a[3]]: x.append([a[0] - 1, a[1], a[2] - 1, a[3]])
            if a[1] <= 10 >= a[3]:
                if s[a[0]][a[1] + 1] * t[a[2]][a[3] + 1]: x.append([a[0], a[1] + 1, a[2], a[3] + 1])
            if -11 < a[1] and -11 < a[3]:
                if s[a[0]][a[1] - 1] * t[a[2]][a[3] - 1]: x.append([a[0], a[1] - 1, a[2], a[3] - 1])
            if a[0] <= 10:
                if s[a[0] + 1][a[1]] * u[a[2] + ~a[0]][a[3] - a[1]]: x.append([a[0] + 1, a[1], a[2], a[3]])
            if -11 < a[0]:
                if s[a[0] - 1][a[1]] * u[a[2] + 1 - a[0]][a[3] - a[1]]: x.append([a[0] - 1, a[1], a[2], a[3]])
            if a[1] <= 10:
                if s[a[0]][a[1] + 1] * u[a[2] - a[0]][a[3] + ~a[1]]: x.append([a[0], a[1] + 1, a[2], a[3]])
            if -11 < a[1]:
                if s[a[0]][a[1] - 1] * u[a[2] - a[0]][a[3] + 1 - a[1]]: x.append([a[0], a[1] - 1, a[2], a[3]])
            if a[2] <= 10:
                if t[a[2] + 1][a[3]] * u[a[2] + 1 - a[0]][a[3] - a[1]]: x.append([a[0], a[1], a[2] + 1, a[3]])
            if -11 < a[2]:
                if t[a[2] - 1][a[3]] * u[a[2] + ~a[0]][a[3] - a[1]]: x.append([a[0], a[1], a[2] - 1, a[3]])
            if a[3] <= 10:
                if t[a[2]][a[3] + 1] * u[a[2] - a[0]][a[3] + 1 - a[1]]: x.append([a[0], a[1], a[2], a[3] + 1])
            if -11 < a[3]:
                if t[a[2]][a[3] - 1] * u[a[2] - a[0]][a[3] + ~a[1]]: x.append([a[0], a[1], a[2], a[3] - 1])
        w, x = x, [];
        z += 1

    # 循环继续。如果当前案例没有解决方案，则输出 -1。
    if z: print(-1)
    a, b, c = map(int, input().split())
