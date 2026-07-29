# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1193: 内存分配
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01193/
# License: not declared; no license is inferred.
import sys
import heapq
from collections import deque
import bisect

def solve():
    # 使用 fast I/O 读取所有输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    it = iter(input_data)
    try:
        N = int(next(it))
    except StopIteration:
        return

    # running_tasks: 存储 [start_address, size, finish_time]，按 start_address 排序
    running_tasks = []
    # finish_heap: 存储所有任务的 finish_time，用于快速找到下一个释放内存的时间
    finish_heap = []
    # wait_queue: 存储等待进程的需求 (size, duration)
    wait_queue = deque()

    wait_count = 0
    total_max_finish_time = 0

    def find_gap(m):
        """寻找长度为 m 的最小起始地址空闲片"""
        if not running_tasks:
            return 0 if N >= m else -1

        # 1. 检查第一个任务之前的空间
        if running_tasks[0][0] >= m:
            return 0

        # 2. 检查任务之间的间隙
        for i in range(len(running_tasks) - 1):
            gap_start = running_tasks[i][0] + running_tasks[i][1]
            gap_end = running_tasks[i+1][0]
            if gap_end - gap_start >= m:
                return gap_start

        # 3. 检查最后一个任务之后的空间
        last_end = running_tasks[-1][0] + running_tasks[-1][1]
        if N - last_end >= m:
            return last_end

        return -1

    def allocate_task(pos, m, finish_t):
        """将任务插入运行列表并更新结束时间堆"""
        nonlocal total_max_finish_time
        # 使用 bisect 保持 running_tasks 按起始地址有序
        bisect.insort(running_tasks, [pos, m, finish_t])
        heapq.heappush(finish_heap, finish_t)
        if finish_t > total_max_finish_time:
            total_max_finish_time = finish_t

    def process_finishes(until_time):
        """处理直到 until_time 为止的所有内存释放和等待队列激活"""
        nonlocal running_tasks
        while finish_heap and finish_heap[0] <= until_time:
            t_f = heapq.heappop(finish_heap)

            # 同时处理所有在 t_f 时刻结束的任务（可能释放出更大的连续空间）
            finish_times_to_clear = {t_f}
            while finish_heap and finish_heap[0] == t_f:
                finish_times_to_clear.add(heapq.heappop(finish_heap))

            # 释放内存
            running_tasks = [t for t in running_tasks if t[2] not in finish_times_to_clear]

            # 优先级最高：检查等待队列队头
            while wait_queue:
                m_q, p_q = wait_queue[0]
                pos = find_gap(m_q)
                if pos != -1:
                    wait_queue.popleft()
                    # 等待队列中的进程从内存释放的时刻 t_f 开始运行
                    allocate_task(pos, m_q, t_f + p_q)
                else:
                    # 如果队头都放不下，根据规则，后面的不能先处理
                    break

    # 主循环：读取每个进程请求
    while True:
        try:
            t_arrival = int(next(it))
            m_size = int(next(it))
            p_duration = int(next(it))
        except StopIteration:
            break

        if t_arrival == 0 and m_size == 0 and p_duration == 0:
            break

        # 1. 在处理新到达请求前，先释放已经完成的任务并处理等待队列
        process_finishes(t_arrival)

        # 2. 尝试分配当前到达的任务
        pos = find_gap(m_size)
        if pos != -1:
            allocate_task(pos, m_size, t_arrival + p_duration)
        else:
            # 放入等待队列
            wait_queue.append((m_size, p_duration))
            wait_count += 1

    # 3. 输入结束后，处理完所有剩余任务
    while finish_heap:
        process_finishes(finish_heap[0])

    # 输出结果
    print(total_max_finish_time)
    print(wait_count)

if __name__ == "__main__":
    solve()
