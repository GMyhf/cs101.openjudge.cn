"""03151 Pots —— special judge。

`python3 -I checker.py <输入> <学生输出> <参考答案>`；退出 0 通过、42 答案错误、3 数据自身出错。

checker 自己对 (x, y) 做 BFS 求最短操作数 K*（或判定到不了），并与参考答案首行核对，
不一致说明数据坏了，退 3 报 Judge Error。学生输出按行读，去掉每行首尾空白、跳过空行：

  · 到不了：必须恰好一行 `impossible`。
  · 到得了：首行是十进制非负整数 K，其后恰好 K 行操作，每行严格是
    `FILL(1)` `FILL(2)` `DROP(1)` `DROP(2)` `POUR(1,2)` `POUR(2,1)` 之一（行内不许有空格）；
    从 (0, 0) 起逐步模拟，结束时某一壶恰好 C 升；且 K == K*。
    参考答案里的具体操作不参与比较，任何最短序列都通过。
"""
import sys
from collections import deque

OPS = ("FILL(1)", "FILL(2)", "DROP(1)", "DROP(2)", "POUR(1,2)", "POUR(2,1)")


def verdict(ok, message):
    print(message)
    sys.exit(0 if ok else 42)


def apply(A, B, state, op):
    x, y = state
    if op == "FILL(1)":
        return A, y
    if op == "FILL(2)":
        return x, B
    if op == "DROP(1)":
        return 0, y
    if op == "DROP(2)":
        return x, 0
    if op == "POUR(1,2)":
        t = min(x, B - y)
        return x - t, y + t
    t = min(y, A - x)
    return x + t, y - t


def shortest(A, B, C):
    dist = {(0, 0): 0}
    queue = deque([(0, 0)])
    while queue:
        state = queue.popleft()
        if C in state:
            return dist[state]
        for op in OPS:
            nxt = apply(A, B, state, op)
            if nxt not in dist:
                dist[nxt] = dist[state] + 1
                queue.append(nxt)
    return None


def lines_of(path):
    text = open(path, "rb").read().decode("utf-8", errors="replace")
    return [line.strip() for line in text.splitlines() if line.strip()]


def main():
    A, B, C = map(int, open(sys.argv[1], encoding="utf-8").read().split()[:3])
    best = shortest(A, B, C)
    reference = lines_of(sys.argv[3])
    expected_first = "impossible" if best is None else str(best)
    if not reference or reference[0] != expected_first:
        print("参考答案与 checker 求出的最短步数不一致"); sys.exit(3)

    out = lines_of(sys.argv[2])
    if not out:
        verdict(False, "输出为空")
    if best is None:
        if out == ["impossible"]:
            verdict(True, "ok")
        verdict(False, "本组无解，应当只输出一行 impossible")
    if out[0] == "impossible":
        verdict(False, "本组有解，不应输出 impossible")
    head = out[0]
    if not (head.isascii() and head.isdigit()) or len(head) > 6:
        verdict(False, "第一行应当是操作数 K")
    k = int(head)
    if len(out) - 1 != k:
        verdict(False, "操作行数与第一行的 K 不一致")
    state = (0, 0)
    for index, op in enumerate(out[1:], 1):
        if op not in OPS:
            verdict(False, f"第 {index} 个操作格式不对（应为 FILL(i)、DROP(i)、POUR(i,j)）")
        state = apply(A, B, state, op)
    if C not in state:
        verdict(False, "执行完这些操作后两个壶里都不是 C 升")
    if k != best:
        verdict(False, "操作序列能得到 C 升，但不是最短的")
    verdict(True, "ok")


main()
