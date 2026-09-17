"""27150 Divisibility by Eight 加强版 —— checker（答案不唯一）。

用法：python3 -I checker.py <输入> <学生输出> <参考答案>；退出 0 通过、42 答案错误，
其他退出码是判题器自身的问题（Judge Error）。

规则（照题面）：
  · 有解时输出 `YES` 再输出一个数；无解时只输出 `NO`。
  · 那个数必须是输入删掉若干位（可以一位都不删）后剩下的子序列，至少一位、全是数字、
    没有前导零（单独一个 `0` 合法），并且能被 8 整除（只看末三位就够）。
  · 有没有解由 checker 自己算：任何一个解的末三位（去掉前导零后）也是解，所以「有解」
    等价于某个 0..992 中 8 的倍数（按不带前导零的写法）是输入的子序列。参考答案只用来
    交叉核对，两者不一致说明数据坏了，退 3 报 Judge Error，不冤判学生。
子序列检查是 `c in iterator` 的线性贪心，200 万位输入加 200 万位输出也在 1 秒内。
"""
import sys


def wrong(message):
    print(message)
    sys.exit(42)


def main():
    digits = open(sys.argv[1], "rb").read().strip()
    try:
        tokens = open(sys.argv[2], "rb").read().split()
    except MemoryError:
        wrong("输出格式不对")
    answer = open(sys.argv[3], "rb").read().split()

    solvable = False
    for value in range(0, 1000, 8):
        position = 0
        for ch in str(value).encode():
            position = digits.find(bytes([ch]), position)
            if position < 0:
                break
            position += 1
        else:
            solvable = True
            break
    if not answer or answer[0] != (b"YES" if solvable else b"NO"):
        print("参考答案与重新计算的有无解不一致")
        sys.exit(3)

    if not tokens:
        wrong("输出为空")
    if tokens[0] == b"NO":
        if len(tokens) != 1:
            wrong("输出 NO 之后不应再有内容")
        if solvable:
            wrong("存在满足条件的删法，不应输出 NO")
        sys.exit(0)
    if tokens[0] != b"YES":
        wrong("第一行应为 YES 或 NO")
    if len(tokens) != 2:
        wrong("输出 YES 之后应恰好再输出一个数")
    if not solvable:
        wrong("不存在满足条件的删法，却输出了 YES")
    number = tokens[1]
    if not number.isdigit():
        wrong("输出的结果不是非负整数")
    if len(number) > 1 and number[:1] == b"0":
        wrong("输出的结果有前导零")
    if int(number[-3:]) % 8:
        wrong("输出的结果不能被 8 整除")
    if len(number) > len(digits):
        wrong("输出的结果不是由原数删去若干位得到的")
    remaining = iter(digits)
    if not all(ch in remaining for ch in number):
        wrong("输出的结果不是由原数删去若干位得到的")
    sys.exit(0)


main()
