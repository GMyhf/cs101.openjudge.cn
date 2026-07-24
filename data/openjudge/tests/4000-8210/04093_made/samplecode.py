# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
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
