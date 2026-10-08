# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1056: IMMEDIATE DECODABILITY
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01056/
# License: not declared; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 参考解：原先引用的 2020fall 代码只在插入时检查「已有编码是当前编码的前缀」，
# 当前编码是已有编码的前缀（如先 01 后 0）时照样判可解码；旧生成器把每组排好序，正好藏住了这个缺陷。
# 这里改成两两比较前缀（每组至多 8 个编码）。
import sys
group = []
k = 0
for t in sys.stdin.read().split():
    if t == "9":
        k += 1
        bad = any(i != j and group[j].startswith(group[i])
                  for i in range(len(group)) for j in range(len(group)))
        print(f"Set {k} is {'not ' if bad else ''}immediately decodable")
        group = []
    else:
        group.append(t)
