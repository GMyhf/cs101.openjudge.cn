"""Codeforces 2173E Shiro's Mirror Duel 交互器。

用法：python3 -I interactor.py <隐藏数据> <参考答案（不读）>

隐藏数据格式（前半段与题面样例输入同形，最后一行是硬币）：
    t
    n            （重复 t 次）
    p_1 ... p_n
    seed K c_1 ... c_K
seed 是硬币随机数种子（random.Random(seed)）；c_1..c_K ∈ {0,1} 是整份文件前 K 次操作的
「剧本硬币」（0 = 不镜像、1 = 镜像），用完后改用 seed 的公平硬币，于是重跑结果确定。
第 0 组用剧本硬币 `0 1` 逐字复现题面 Note 的两次回应。

交互：先发 t，每组发 n 与 p。选手每次输出 `? x y`（1 ≤ x ≠ y ≤ n），交互器掷硬币，
交换 (x, y) 或 (n-x+1, n-y+1)，回应实际交换的那对下标（顺序与 x、y 对应）。
选手输出 `!` 结束本组，此时 p 必须升序；每组 `?` 至多 ⌊2.5n+800⌋ 次（`!` 不计）。
按 token 读（与 testlib 一致，换行无所谓）。最后一组 `!` 之后立即退出，之后的多余输出不看。

退出码：0 通过，42 答案错误（格式错、下标越界、x = y、超次数、未排好序、提前结束）。
stderr 最后一行是给学生的一句话，不含测试数据。
"""
import random
import re
import sys

INT = re.compile(r"-?\d{1,19}\Z")


def wrong(message):
    print(message, file=sys.stderr)
    sys.exit(42)


def say(text):
    try:
        sys.stdout.write(text)
        sys.stdout.flush()
    except (BrokenPipeError, OSError):
        wrong("程序提前结束")


def tokens():
    while True:
        try:
            line = sys.stdin.readline()
        except (OSError, UnicodeDecodeError, ValueError):
            line = ""
        if not line:
            return
        yield from line.split()


def main():
    data = open(sys.argv[1]).read().split()
    t = int(data[0])
    pos = 1
    tests = []
    for _ in range(t):
        n = int(data[pos])
        tests.append((n, [int(v) for v in data[pos + 1:pos + 1 + n]]))
        pos += 1 + n
    seed, k = int(data[pos]), int(data[pos + 1])
    script = [int(v) for v in data[pos + 2:pos + 2 + k]]
    rng = random.Random(seed)
    ops_total = 0
    stream = tokens()

    def nxt():
        token = next(stream, None)
        if token is None:
            wrong("程序提前结束（没有输出 `!` 就退出了）")
        return token

    say(f"{t}\n")
    worst = 0
    for case_no, (n, p) in enumerate(tests, 1):
        p = [0] + p
        say(f"{n}\n{' '.join(map(str, p[1:]))}\n")
        limit = (5 * n + 1600) // 2
        used = 0
        while True:
            token = nxt()
            if token == "!":
                break
            if token != "?":
                wrong(f"第 {case_no} 组：期望 `?` 或 `!`，读到了别的内容")
            xs, ys = nxt(), nxt()
            if not (INT.match(xs) and INT.match(ys)):
                wrong(f"第 {case_no} 组：`?` 后面应是两个整数")
            x, y = int(xs), int(ys)
            if not (1 <= x <= n and 1 <= y <= n) or x == y:
                wrong(f"第 {case_no} 组：下标必须满足 1 ≤ x ≠ y ≤ n")
            used += 1
            if used > limit:
                wrong(f"第 {case_no} 组：操作超过 ⌊2.5n+800⌋ = {limit} 次")
            if ops_total < len(script):
                mirror = script[ops_total]
            else:
                mirror = rng.getrandbits(1)
            ops_total += 1
            if mirror:
                x, y = n - x + 1, n - y + 1
            p[x], p[y] = p[y], p[x]
            say(f"{x} {y}\n")
        if any(p[i] != i for i in range(1, n + 1)):
            wrong(f"第 {case_no} 组：输出 `!` 时排列还没有排好序")
        worst = max(worst, used * 1000 // limit)
    print(f"通过：单组操作次数最多用到上限的 {worst / 10:.1f}%", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
