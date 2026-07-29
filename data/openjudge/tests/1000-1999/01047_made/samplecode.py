# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1047: Round and Round We Go
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01047/
# License: not declared; no license is inferred.
import sys
# 24-物院-彭博
def generate_rotations(s):
    return {s[i:] + s[:i] for i in range(len(s))}


while True:
    try:
        n = input()
        length, num = len(n), int(n)
        rotations = generate_rotations(n)

        flag = True
        for i in range(2, length + 1):
            n_ = str(num * i)
            if n_ not in rotations and "0" + n_ not in rotations:
                flag = False
                break

        if flag:
            print(f"{n} is cyclic")
        else:
            print(f"{n} is not cyclic")

    except EOFError:
        break
