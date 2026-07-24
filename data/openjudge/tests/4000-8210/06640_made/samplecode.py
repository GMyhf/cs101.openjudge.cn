# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
from collections import defaultdict
def main():
    n = int(input())
    index = 1
    inverted_index = defaultdict(set)   # 构建倒排索引
    for i in range(1, n + 1):
        parts = input().split()
        doc_id = i
        num_words = int(parts[0])
        words = parts[1:num_words + 1]
        for word in words:
            inverted_index[word].add(doc_id)

    m = int(input())
    results = []

    # 查询倒排索引
    for _ in range(m):
        query = input()
        if query in inverted_index:
            results.append(" ".join(map(str, sorted(list(inverted_index[query])))))
        else:
            results.append("NOT FOUND")

    # 输出查询结果
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
