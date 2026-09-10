# Written for this repository from the public problem statement; no external submission used.
# 1374C Move Brackets —— 答案就是「扫一遍时前缀和变负的次数」，即失配的右括号个数。
import sys


def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    cursor = 1
    answers = []
    for _ in range(t):
        n = int(data[cursor])
        text = data[cursor + 1]
        cursor += 2
        balance = moves = 0
        for char in text[:n]:
            balance += 1 if char == "(" else -1
            if balance < 0:
                moves += 1
                balance = 0
        answers.append(str(moves))
    sys.stdout.write("\n".join(answers) + "\n")


main()
