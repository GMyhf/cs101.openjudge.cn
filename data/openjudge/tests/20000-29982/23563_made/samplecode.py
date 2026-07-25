# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# 2022fall-cs101, 楼翔
import re
intermedia = input()
listy = [int(x) for x in re.findall(r".(?<!\+0)n\^(\d+)", intermedia)] + [0]
print("n^" + str(max(listy)))
