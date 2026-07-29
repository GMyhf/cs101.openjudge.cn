# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2899: 矩阵交换行
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02899/
# License: not declared; no license is inferred.
import sys
def swap_rows(matrix, n, m):
    # 检查 n 和 m 是否在矩阵的有效索引范围内
    if n < 0 or n >= 5 or m < 0 or m >= 5:
        return 0
    # 交换矩阵的第 n 行和第 m 行
    matrix[n], matrix[m] = matrix[m], matrix[n]
    return 1


def main():
    matrix = []
    # 读取 5 行输入，每行输入代表矩阵的一行
    for _ in range(5):
        # 将输入按空格分割成多个元素，并转换为整数列表
        row = list(map(int, input().split()))
        matrix.append(row)
    # 读取 n 和 m 的值
    n, m = map(int, input().split())
    # 调用 swap_rows 函数进行行交换操作
    result = swap_rows(matrix, n, m)
    if result == 0:
        print("error")
    else:
        # 遍历矩阵的每一行
        for row in matrix:
            # 格式化输出每行元素，每个元素宽度为 4
            formatted_row = [f"{num:4d}" for num in row]
            # 将格式化后的元素用空字符串连接起来并输出
            print("".join(formatted_row))


if __name__ == "__main__":
    main()
