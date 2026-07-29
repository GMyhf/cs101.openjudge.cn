# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2814: 拨钟问题
# Fenced code block index: 4
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02814/
# License: not declared; no license is inferred.
import sys
import sys

def solve():
    # 读取输入的9个整数（时钟初始状态）
    try:
        input_data = sys.stdin.read().split()
        if not input_data:
            return
        clocks = [int(x) for x in input_data]
    except EOFError:
        return

    # 变量 m1, m2, ..., m9 分别代表移动 1-9 执行的次数 (0-3次)
    # 根据题目给出的“移动影响的时钟”，我们可以推导出每个时钟受哪些移动的影响：
    # A (index 0): 1, 2, 4
    # B (index 1): 1, 2, 3, 5
    # C (index 2): 2, 3, 6
    # D (index 3): 1, 4, 5, 7
    # E (index 4): 1, 3, 5, 7, 9
    # F (index 5): 3, 5, 6, 9
    # G (index 6): 4, 7, 8
    # H (index 7): 5, 7, 8, 9
    # I (index 8): 6, 8, 9

    # 使用嵌套循环进行穷举。为了提速，我们在循环中间进行判断（剪枝）
    for m1 in range(4):
        for m2 in range(4):
            for m3 in range(4):
                for m4 in range(4):
                    # 检查时钟 A 是否能回到12点（0点）
                    if (clocks[0] + m1 + m2 + m4) % 4 != 0:
                        continue
                    for m5 in range(4):
                        # 检查时钟 B
                        if (clocks[1] + m1 + m2 + m3 + m5) % 4 != 0:
                            continue
                        for m6 in range(4):
                            # 检查时钟 C
                            if (clocks[2] + m2 + m3 + m6) % 4 != 0:
                                continue
                            for m7 in range(4):
                                # 检查时钟 D
                                if (clocks[3] + m1 + m4 + m5 + m7) % 4 != 0:
                                    continue
                                for m8 in range(4):
                                    # 检查时钟 G
                                    if (clocks[6] + m4 + m7 + m8) % 4 != 0:
                                        continue
                                    for m9 in range(4):
                                        # 检查剩余时钟 E, F, H, I
                                        if (clocks[4] + m1 + m3 + m5 + m7 + m9) % 4 != 0: continue
                                        if (clocks[5] + m3 + m5 + m6 + m9) % 4 != 0: continue
                                        if (clocks[7] + m5 + m7 + m8 + m9) % 4 != 0: continue
                                        if (clocks[8] + m6 + m8 + m9) % 4 != 0: continue

                                        # 找到解，格式化输出
                                        counts = [m1, m2, m3, m4, m5, m6, m7, m8, m9]
                                        result = []
                                        for i in range(9):
                                            for _ in range(counts[i]):
                                                result.append(str(i + 1))
                                        print(" ".join(result))
                                        return

if __name__ == "__main__":
    solve()
