# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1062: 昂贵的聘礼
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01062/
# License: not declared; no license is inferred.
# 2300015881 赵凌哲 光华管理学院
def dfs(num, max_level, min_level):
    if item_list[num][3]:
        return -1
    if item_list[num][1] < max_level - m or item_list[num][1] > min_level + m:
        return -1
    item_list[num][3] = True
    max_level_updated = max(max_level, item_list[num][1])
    min_level_updated = min(min_level, item_list[num][1])
    price = item_list[num][0]
    for replace_item in item_list[num][2]:
        pr = dfs(replace_item[0], max_level_updated, min_level_updated)
        if pr == -1:
            continue
        else:
            price = min(price, replace_item[1] + pr)
    item_list[num][3] = False
    return price


m, n = map(int, input().split())
item_list = []
for i in range(n):
    p, l, x = map(int, input().split())
    replace_options = []
    for j in range(x):
        t, v = map(int, input().split())
        replace_options.append([t - 1, v])
    item_list.append([p, l, replace_options, False])
print(dfs(0, item_list[0][1], item_list[0][1]))
