"""Codeforces 1793C Dora and Search —— checker（答案不唯一）。

用法：python3 -I checker.py <输入> <学生输出> <参考答案>；退出 0 通过、42 答案错误，
其他退出码是判题器自身的问题（Judge Error）。

规则（照题面）：多组数据，每组要么输出 `-1`（不存在合法区间），要么输出两个下标 l r，
满足 1 ≤ l ≤ r ≤ n，且 a_l、a_r 都既不是 a[l..r] 的最小值也不是最大值。
  · 有没有解由 checker 自己用双指针收缩重算；参考答案只用来交叉核对（逐组的 -1 与否），
    不一致退 3（Judge Error），不冤判学生。
  · 学生输出按 token 顺序读：遇到 `-1` 占一个 token，否则取两个十进制整数；
    token 数必须恰好用完。任何格式问题一律判答案错误。
"""
import re
import sys

INDEX = re.compile(rb"[0-9]{1,7}")


def wrong(message):
    print(message)
    sys.exit(42)


def solvable(a):
    l, r, lo, hi = 0, len(a) - 1, 1, len(a)
    while l < r:
        if a[l] == lo:
            l += 1; lo += 1
        elif a[l] == hi:
            l += 1; hi -= 1
        elif a[r] == lo:
            r -= 1; lo += 1
        elif a[r] == hi:
            r -= 1; hi -= 1
        else:
            return True
    return False


def main():
    data = open(sys.argv[1], "rb").read().split()
    tokens = open(sys.argv[2], "rb").read().split()
    answer = open(sys.argv[3], "rb").read().split()
    t = int(data[0]); p = 1; q = 0; s = 0
    for case in range(1, t + 1):
        n = int(data[p]); a = list(map(int, data[p + 1:p + 1 + n])); p += 1 + n
        exists = solvable(a)
        if s >= len(answer) or (answer[s] == b"-1") == exists:
            print("参考答案与重新计算的有无解不一致")
            sys.exit(3)
        s += 1 if answer[s] == b"-1" else 2
        if q >= len(tokens):
            wrong(f"第 {case} 组数据没有输出")
        if tokens[q] == b"-1":
            q += 1
            if exists:
                wrong(f"第 {case} 组数据存在合法区间，不应输出 -1")
            continue
        if q + 1 >= len(tokens) or not INDEX.fullmatch(tokens[q]) or not INDEX.fullmatch(tokens[q + 1]):
            wrong(f"第 {case} 组数据应输出 -1 或两个下标")
        l, r = int(tokens[q]), int(tokens[q + 1]); q += 2
        if not 1 <= l <= r <= n:
            wrong(f"第 {case} 组数据的下标不满足 1 ≤ l ≤ r ≤ n")
        segment = a[l - 1:r]
        lo, hi = min(segment), max(segment)
        if a[l - 1] in (lo, hi) or a[r - 1] in (lo, hi):
            wrong(f"第 {case} 组数据输出的区间端点是区间的最小值或最大值")
    if s != len(answer):
        print("参考答案的组数与输入不符")
        sys.exit(3)
    if q != len(tokens):
        wrong("输出的内容多于数据组数")
    sys.exit(0)


main()
