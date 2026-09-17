"""02982 Sudoku checker：解不唯一时任一合法填法都算对。

用法：python3 -I checker.py <输入> <学生输出> <参考答案>；退出 0 通过、42 答案错误。
逐组要求：9 个 9 位的 1..9 数字串；每行、每列、每个 3x3 宫都是 1..9 的排列；
题目给出的非 0 格保持原值。参考答案不参与判定（每组输入都保证有解，构建时已验证）。
"""
import sys

WA = 42


def reject(message):
    print(message)
    sys.exit(WA)


def main():
    tokens = open(sys.argv[1], encoding="utf-8").read().split()
    t = int(tokens[0])
    puzzles = tokens[1:1 + 9 * t]
    with open(sys.argv[2], "rb") as handle:
        raw = handle.read(4 * 1024 * 1024 + 1)
    if len(raw) > 4 * 1024 * 1024:
        reject("输出过长")
    got = raw.decode("utf-8", errors="replace").split()
    if len(got) < 9 * t:
        reject("输出的行数不够：应当每组 9 行")
    if len(got) > 9 * t:
        reject("输出有多余的内容")
    digits = set("123456789")
    for k in range(t):
        case = got[9 * k:9 * k + 9]
        for line in case:
            if len(line) != 9 or not set(line) <= digits:
                reject(f"第 {k + 1} 组：每行应当是 9 个 1~9 的数字")
        for r in range(9):
            given = puzzles[9 * k + r]
            for c in range(9):
                if given[c] != "0" and given[c] != case[r][c]:
                    reject(f"第 {k + 1} 组：改动了题目已给出的数字")
        for r in range(9):
            if set(case[r]) != digits:
                reject(f"第 {k + 1} 组：某一行有重复数字")
        for c in range(9):
            if {case[r][c] for r in range(9)} != digits:
                reject(f"第 {k + 1} 组：某一列有重复数字")
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                if {case[br + i][bc + j] for i in range(3) for j in range(3)} != digits:
                    reject(f"第 {k + 1} 组：某个 3x3 宫有重复数字")
    sys.exit(0)


main()
