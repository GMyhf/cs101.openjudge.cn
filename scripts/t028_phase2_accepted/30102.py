# External reference: http://cs101.openjudge.cn/practice/30102/statistics/
# Accepted submission: 52789464
# Source: http://cs101.openjudge.cn/practice/solution/52789464/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 优化读取：sys.stdin.read().split() 处理百万级整数最快
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    # 转换为整数列表，prices[r] 代表第 r 秒的价格
    prices = [int(x) for x in input_data[1:n+1]]

    # 添加哨兵值 -1，确保循环结束时强制弹出栈中所有元素进行结算
    prices.append(-1)

    # buy_stack 存储：[买入点下标, 该点所覆盖区域内的最大值下标]
    # 这是一个单调递增栈，保证栈底到栈顶价格由低到高
    buy_stack = []
    max_window_len = 0

    # 性能优化：缓存 list 的方法，减少循环内的属性查找开销
    pop_entry = buy_stack.pop
    push_entry = buy_stack.append

    for r in range(n + 1):
        current_price = prices[r]
        # right_max_idx 作为“接力棒”，记录当前买入点右侧区域中的最大值索引
        # 初始指向当前扫描位置 r
        right_max_idx = r

        # 当当前价格 <= 栈顶价格，说明栈顶作为“唯一最小值”的统治结束
        while buy_stack and prices[buy_stack[-1][0]] >= current_price:
            # buy_idx: 潜在的买入点位置
            # sub_range_max_idx: buy_idx 到它在栈中上一个元素之间曾经出现过的最大值位置
            buy_idx, sub_range_max_idx = pop_entry()

            # 计算逻辑：如果 right_max_idx 已经更新（不再是 r），
            # 说明在 buy_idx 的右侧存在比它大的潜在卖出点
            if right_max_idx != r:
                # 盈利验证与长度计算
                # 区间 [buy_idx, right_max_idx] 即为一个候选的完美交易窗口
                current_len = right_max_idx - buy_idx + 1
                if current_len > max_window_len:
                    max_window_len = current_len

            # 更新接力棒：比较当前弹出的局部最大值和已知的右侧最大值
            # 保证向左传递的过程中，right_max_idx 始终指向已发现的最强卖出点
            if prices[sub_range_max_idx] > prices[right_max_idx]:
                right_max_idx = sub_range_max_idx

        # 将当前位置压入栈，初始最大值位置就是它自己
        push_entry([r, right_max_idx])

    # 输出最终记录的最长窗口秒数
    sys.stdout.write(str(max_window_len) + '\n')

if __name__ == "__main__":
    solve()
