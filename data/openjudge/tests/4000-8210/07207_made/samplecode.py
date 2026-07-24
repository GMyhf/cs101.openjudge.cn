# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def construct_magic_square(N):
    M = 2 * N - 1
    # 创建 M x M 的矩阵，初始为0
    magic = [[0] * M for _ in range(M)]

    # 初始位置：第一行，中间列
    row, col = 0, M // 2
    magic[row][col] = 1

    # 填充 2 到 M*M
    for num in range(2, M * M + 1):
        # 计算下一个位置：上一行，右一列（边界循环）
        next_row = (row - 1) % M
        next_col = (col + 1) % M

        # 如果目标位置已经有数字，就放在正下方
        if magic[next_row][next_col] != 0:
            next_row = (row + 1) % M  # 正下方，注意也可能越界，用 % M
            next_col = col

        # 放置当前数字
        magic[next_row][next_col] = num
        # 更新当前位置
        row, col = next_row, next_col

    return magic


def print_magic_square(magic):
    M = len(magic)
    for i in range(M):
        # 将每行数字转为字符串，用空格连接
        print(" ".join(str(magic[i][j]) for j in range(M)))


# 主程序
if __name__ == "__main__":
    N = int(input().strip())
    square = construct_magic_square(N)
    print_magic_square(square)
