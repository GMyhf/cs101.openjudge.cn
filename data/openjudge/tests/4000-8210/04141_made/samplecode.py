# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# 原为 蒋子轩23工学院 的 DFS 写法（按每种砝码的枚数逐一枚举，组合数是各 (ai+1) 之积）。
# 2026-10-07 审计：数据加了总重贴近 1000 的满规模组，DFS 要枚举上亿种组合、单组跑数十秒，
# 换成与 producecase.py 内嵌 REFERENCE_SOURCE 相同的按重量可达性 DP；原 DFS 仍保留在
# producecase.py 的 DFS_SOURCE 里，第 0..19 组两者输出一致。
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
a = list(map(int, input().split()))
w = (1, 2, 3, 5, 10, 20)
ok = [True] + [False] * 1000
for cnt, wt in zip(a, w):
    for _ in range(cnt):
        for x in range(1000, wt - 1, -1):
            if ok[x - wt]:
                ok[x] = True
print(f'Total={sum(ok) - 1}')
