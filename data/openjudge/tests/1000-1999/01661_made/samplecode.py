# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1661: Help Jimmy
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01661/
# License: not declared in source collection; no license is inferred.
import sys
import sys
from functools import lru_cache

# 优化1：增加递归深度限制，防止 N=1000 时爆栈
sys.setrecursionlimit(2000)

def solve():
    # 优化2：使用 sys.stdin.read 快速读取所有输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)

    try:
        num_test_cases = int(next(iterator))
    except StopIteration:
        return

    for _ in range(num_test_cases):
        try:
            N = int(next(iterator))
            ini_x = int(next(iterator))
            ini_y = int(next(iterator))
            MaxVal = int(next(iterator))

            p = []
            for _ in range(N):
                p.append((int(next(iterator)), int(next(iterator)), int(next(iterator))))

            # 按高度从大到小排序
            p.sort(key=lambda x: -x[2])

            @lru_cache(None)
            def dfs(x, y, parent_idx):
                # parent_idx: 刚离开的平台索引（如果是起点则为 -1）
                # 需要在 p[parent_idx+1 ... N] 中寻找接住我们的平台

                for i in range(parent_idx + 1, N):
                    px1, px2, ph = p[i]

                    # 剪枝：因为 p 是按高度从大到小排的
                    # 如果当前平台的高度差已经超过 MaxVal，那后面更低的平台肯定也接不住，直接死掉
                    if y - ph > MaxVal:
                        return float('inf')

                    # 判断横坐标是否在平台范围内
                    if px1 <= x <= px2:
                        # 找到了接住的平台 i
                        # 递归计算：(当前位置到平台左/右端的水平距离) + dfs(下一层)
                        # 注意：题目求时间，垂直时间恒为 total_Y，这里 dfs 只负责计算最小水平距离

                        dist_left = x - px1 + dfs(px1, ph, i)
                        dist_right = px2 - x + dfs(px2, ph, i)
                        return min(dist_left, dist_right)

                # 如果循环结束都没 break，说明落到了地面 (y=0)
                if y <= MaxVal:
                    return 0
                else:
                    return float('inf')

            # 初始调用：从 (ini_x, ini_y) 开始，父节点索引传 -1，
            # 这样循环会从 0 (第一个平台) 开始搜索
            min_horizontal_dist = dfs(ini_x, ini_y, -1)

            if min_horizontal_dist == float('inf'):
                # 理论上题目保证有解，不会进这里
                pass
            else:
                # 总时间 = 垂直下落距离(ini_y) + 最小水平移动距离
                print(ini_y + min_horizontal_dist)

        except StopIteration:
            break

if __name__ == '__main__':
    solve()
