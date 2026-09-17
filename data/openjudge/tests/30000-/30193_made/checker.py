"""30193 哈密顿激活层 checker：题面「如果存在多种方案，输出任意一种即可。如果不存在可行方案，输出 -1。」

用法：python3 -I checker.py <输入> <学生输出> <参考答案>；退出 0 通过、42 答案错误、3 = 参考答案自身有问题。

· 参考答案是 -1（构建时由参考解穷尽搜索并经独立实现复核）：学生输出必须恰好是 `-1`。
  若学生给出了一条合法路径，说明参考答案错了 —— 退 3（Judge Error），不冤判学生。
· 参考答案是一条路径：学生输出 -1 判错；否则必须恰好 N×M−B 对整数 `r c`，逐步检查：
  在界内、不是坏死区、不重复（于是恰好覆盖全部正常格）、相邻两步曼哈顿距离为 1、
  每个锁定的 (r, c, t) 在第 t 步恰好位于 (r, c)。
按空白切分 token，不计行结构。
"""
import re
import sys

WA = 42
MAX_BYTES = 16 * 1024 * 1024
INT = re.compile(r"-?[0-9]{1,6}\Z")


def reject(message):
    print(message)
    sys.exit(WA)


def broken(message):
    print("判题数据有误")
    sys.stderr.write(message + "\n")
    sys.exit(3)


def problem(tokens, n, m, locks, blocked):
    """学生 token 不是合法激活路径时返回原因，合法时返回 None。"""
    total = n * m - len(blocked)
    if len(tokens) != 2 * total:
        return "输出的坐标个数不等于正常神经元个数"
    if not all(INT.match(x) for x in tokens):
        return "输出应当全是整数坐标"
    values = [int(x) for x in tokens]
    seen = set()
    prev = None
    for step in range(1, total + 1):
        r, c = values[2 * step - 2], values[2 * step - 1]
        if not (1 <= r <= n and 1 <= c <= m):
            return f"第 {step} 步坐标越界"
        if (r, c) in blocked:
            return f"第 {step} 步走进了坏死区"
        if (r, c) in seen:
            return f"第 {step} 步重复激活了同一个神经元"
        seen.add((r, c))
        if prev is not None and abs(r - prev[0]) + abs(c - prev[1]) != 1:
            return f"第 {step} 步与上一步不相邻"
        want = locks.get(step)
        if want is not None and want != (r, c):
            return f"第 {step} 步没有到达被锁定的神经元"
        prev = (r, c)
    return None


def main():
    data = open(sys.argv[1], encoding="utf-8").read().split()
    n, m, k, b = (int(x) for x in data[:4])
    p = 4
    locks = {}
    for _ in range(k):
        r, c, t = int(data[p]), int(data[p + 1]), int(data[p + 2])
        locks[t] = (r, c)
        p += 3
    blocked = set()
    for _ in range(b):
        blocked.add((int(data[p]), int(data[p + 1])))
        p += 2
    answer = open(sys.argv[3], encoding="utf-8").read().split()
    with open(sys.argv[2], "rb") as handle:
        raw = handle.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        reject("输出过长")
    got = raw.decode("utf-8", errors="replace").split()
    if not got:
        reject("输出为空")
    if answer == ["-1"]:
        if got == ["-1"]:
            sys.exit(0)
        if problem(got, n, m, locks, blocked) is None:
            broken("学生给出了合法路径，参考答案却是 -1")
        reject("答案错误：本组可行性判断有误或输出格式不对")
    if got == ["-1"]:
        reject("存在可行的激活方案，却输出了 -1")
    reason = problem(got, n, m, locks, blocked)
    if reason is not None:
        reject(reason)
    sys.exit(0)


main()
