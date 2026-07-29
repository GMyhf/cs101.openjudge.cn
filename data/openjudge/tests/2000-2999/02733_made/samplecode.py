# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2733: 判断闰年
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/02733/
# License: not declared in source collection; no license is inferred.
import sys
# 2022cs101, 高靖，城市与环境学院
# 四年一闰，百年不闰，四百年再闰

a=int(input())

if a%4==0:
    if a%100==0:
        if a%400==0:
            print("Y")
        else:
            print("N")
    else:
        print("Y")
else:
    print("N")
