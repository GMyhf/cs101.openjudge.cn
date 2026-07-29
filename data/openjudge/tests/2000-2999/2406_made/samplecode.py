# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2406: 字符串乘方
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02406/
# License: not declared in source collection; no license is inferred.
while True:
    s = input().strip()
    if s == '.':
        break
    len_s = len(s)
    max_power = 1
    for i in range(1, len_s // 2 + 1):
        if len_s % i == 0:
            a = s[:i]
            if a * (len_s // i) == s:
                max_power = max(max_power, len_s // i)
    print(max_power)
