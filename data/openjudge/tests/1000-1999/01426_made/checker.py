"""01426 Find The Multiple —— special judge。

`python3 -I checker.py <输入> <学生输出> <参考答案>`；退出 0 通过、42 答案错误。

输入是若干个 n（1..200），读到 0 为止。学生输出按空白切成 token，个数必须恰好等于 n 的
个数，第 k 个 token 要：只含 ASCII 0/1、首位是 1（非零、无前导零，与原站 val.cpp 同）、
不超过 100 位、是第 k 个 n 的倍数。参考答案只用来核对题数，不拿它比对数值 ——
任何合法倍数都通过。给学生的话不带 n 的值与组号以外的数据。
"""
import sys

MAX_DIGITS = 100


def verdict(ok, message):
    print(message)
    sys.exit(0 if ok else 42)


def main():
    ns = []
    for token in open(sys.argv[1], encoding="utf-8").read().split():
        if int(token) == 0:
            break
        ns.append(int(token))
    answer = open(sys.argv[3], "rb").read().split()
    if len(answer) != len(ns):              # 数据自身出错：退 3，报 Judge Error 而不是冤判
        print("参考答案与输入组数不符")
        sys.exit(3)
    tokens = open(sys.argv[2], "rb").read().split()
    if len(tokens) < len(ns):
        verdict(False, f"输出只有 {len(tokens)} 个数，少于询问个数")
    if len(tokens) > len(ns):
        verdict(False, "输出的数多于询问个数")
    for index, (n, token) in enumerate(zip(ns, tokens), 1):
        if len(token) > MAX_DIGITS:
            verdict(False, f"第 {index} 个答案超过 100 位")
        if token.strip(b"01") or token[:1] != b"1":
            verdict(False, f"第 {index} 个答案不是只含 0 和 1、首位为 1 的正整数")
        if int(token) % n:
            verdict(False, f"第 {index} 个答案不是 n 的倍数")
    verdict(True, "ok")


main()
