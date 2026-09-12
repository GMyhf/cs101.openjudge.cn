#!/usr/bin/env python3
# 04093 倒排索引查询 —— 参考实现。
#
# 来源：仓库交接件。算法与代码取自课程题解集
# `/home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md`（人交付进本仓库的材料，
# 不是平台提交，所以不写提交号、也不套用外部许可）。2026-09-12 只改了头部注释，
# 算法一行没动。
#
# 注意一处**题面保证兜住的边界**：题面明写「数据保证每行至少出现一个 1」，所以
# 「一个 1 都没有」的查询在合法输入里不存在。这份实现把它当 NOT FOUND，而「全集减去
# 排除项」同样说得通 —— 两种写法在合法输入上完全等价。2026-09-12 之前生成器没有
# `valid()`，真的生成了 22 条一个 1 都没有的查询，于是这份数据会把后一种写法判成
# Wrong Answer（实测挂第 2 组）。数据已按题面重建，见 CHANGELOG。
import sys
input = sys.stdin.read
data = input().split()

index = 0
N = int(data[index])
index += 1

word_documents = []

# 读取每个词的倒排索引
for _ in range(N):
    ci = int(data[index])
    index += 1
    documents = sorted(map(int, data[index:index + ci]))
    index += ci
    word_documents.append(documents)

M = int(data[index])
index += 1

results = []

# 处理每个查询
for _ in range(M):
    query = list(map(int, data[index:index + N]))
    index += N

    # 集合存储各词的文档集合（使用交集获取所有词都出现的文档）
    included_docs = []
    excluded_docs = set()

    # 解析查询条件
    for i in range(N):
        if query[i] == 1:
            included_docs.append(word_documents[i])
        elif query[i] == -1:
            excluded_docs.update(word_documents[i])

    # 仅在有包含词时计算交集
    if included_docs:
        result_set = set(included_docs[0])
        for docs in included_docs[1:]:
            result_set.intersection_update(docs)
        result_set.difference_update(excluded_docs)
        final_docs = sorted(result_set)
        results.append(" ".join(map(str, final_docs)) if final_docs else "NOT FOUND")
    else:
        results.append("NOT FOUND")

# 输出所有查询结果
for result in results:
    print(result)
