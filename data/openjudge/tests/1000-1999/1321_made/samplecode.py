# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1321: 棋盘问题
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01321/
# License: not declared in source collection; no license is inferred.
def place_pieces(n, k, row, board, cols, count):
    # 如果已经放置了k个棋子，计数加一
    if k == 0:
        count[0] += 1
        return

    # 从当前行row开始尝试
    for i in range(row, n):
        # 遍历该行所有列
        for j in range(n):
            # 如果当前位置是可放棋子的地方，并且没有放置在该列，且该行还没被用过
            if board[i][j] == '#' and not cols[j]:
                # 放置棋子，标记该行和该列
                cols[j] = 1
                place_pieces(n, k - 1, i + 1, board, cols, count)
                # 回溯，撤销棋子的放置
                cols[j] = 0

def main():
    while True:
        # 读取 n 和 k
        n, k = map(int, input().split())
        if n == -1 and k == -1:
            break

        # 读取棋盘形状
        board = [input().strip() for _ in range(n)]

        # 用来记录列的状态，0 表示该列没有放棋子，1 表示该列已放置棋子
        cols = [0] * n
        count = [0]  # 计数器，存储可行的方案数

        place_pieces(n, k, 0, board, cols, count)

        print(count[0])

if __name__ == "__main__":
    main()
