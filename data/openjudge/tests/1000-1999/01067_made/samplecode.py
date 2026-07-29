# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1067: 取石子游戏
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01067/
# License: not declared; no license is inferred.
import math

def wythoff(a, b):
    if a > b:
        a, b = b, a  # Make sure a <= b.
    k = b - a
    ak = k * (math.sqrt(5) + 1) / 2  # ak is the k-th element in the Beatty sequence.
    return 1 if a != int(ak) else 0

while True:
    try:
        a, b = map(int, input().split())
    except:
        break

    ans = wythoff(a, b)

    print(ans)
