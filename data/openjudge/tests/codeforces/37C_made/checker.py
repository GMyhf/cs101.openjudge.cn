"""Codeforces 37C Old Berland Language —— checker（答案不唯一）。

用法：python3 -I checker.py <输入> <学生输出> <参考答案>；退出 0 通过、42 答案错误，
其他退出码是判题器自身的问题（Judge Error）。

规则（照题面）：
  · 无解时只输出 `NO`；有解时输出 `YES`，再按输入顺序输出 N 个只含 0/1 的词，
    第 i 个词长度恰为 l_i，任何一个词都不是另一个词的前缀（相同的两个词也算）。
  · 有没有解由 checker 自己按 Kraft 不等式 Σ2^(-l_i) ≤ 1 精确（整数）计算；
    参考答案只用来交叉核对，不一致退 3（Judge Error），不冤判学生。
前缀检查：把词排序后，若 a 是 b 的前缀，则排在 a、b 之间的词都以 a 开头，所以只查相邻两个。
"""
import sys


def wrong(message):
    print(message)
    sys.exit(42)


def main():
    data = open(sys.argv[1], "rb").read().split()
    n = int(data[0])
    lengths = [int(x) for x in data[1:1 + n]]
    tokens = open(sys.argv[2], "rb").read().split()
    answer = open(sys.argv[3], "rb").read().split()

    top = max(lengths)
    solvable = sum(1 << (top - l) for l in lengths) <= (1 << top)
    if not answer or answer[0] != (b"YES" if solvable else b"NO"):
        print("参考答案与重新计算的有无解不一致")
        sys.exit(3)

    if not tokens:
        wrong("输出为空")
    if tokens[0] == b"NO":
        if len(tokens) != 1:
            wrong("输出 NO 之后不应再有内容")
        if solvable:
            wrong("这组长度可以构造出词表，不应输出 NO")
        sys.exit(0)
    if tokens[0] != b"YES":
        wrong("第一行应为 YES 或 NO")
    if not solvable:
        wrong("这组长度构造不出词表，却输出了 YES")
    if len(tokens) != n + 1:
        wrong("YES 之后输出的词数不等于 N")
    words = tokens[1:]
    for index, word in enumerate(words):
        if len(word) != lengths[index]:
            wrong(f"第 {index + 1} 个词的长度与输入不符")
        if word.strip(b"01"):
            wrong(f"第 {index + 1} 个词含有 0/1 以外的字符")
    ordered = sorted(words)
    for a, b in zip(ordered, ordered[1:]):
        if b.startswith(a):
            wrong("有一个词是另一个词的前缀")
    sys.exit(0)


main()
