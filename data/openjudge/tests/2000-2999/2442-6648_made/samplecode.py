# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 2442: Sequence
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02442/
# License: not declared in source collection; no license is inferred.
import sys
import heapq

def get_ints():
    """从标准输入流中逐词读取整数，节省内存。"""
    for line in sys.stdin:
        for word in line.split():
            yield word

def solve():
    ints_gen = get_ints()

    try:
        token = next(ints_gen)
    except StopIteration:
        return

    # 测试用例数量
    t_cases = int(token)

    for _ in range(t_cases):
        try:
            m = int(next(ints_gen))
            n = int(next(ints_gen))
        except StopIteration:
            break

        # 读取第一个序列并排序
        res = []
        for i in range(n):
            res.append(int(next(ints_gen)))
        res.sort()

        # 依次合并剩余的 m-1 个序列
        for _ in range(m - 1):
            row = []
            for i in range(n):
                row.append(int(next(ints_gen)))
            row.sort()

            # 使用最小堆合并当前结果 res 和新序列 row
            # 堆中存储: (和, row序列的索引, res序列的值)
            h = [(res[i] + row[0], 0, res[i]) for i in range(n)]
            heapq.heapify(h)

            new_res = [0] * n
            for k in range(n):
                curr_sum, row_idx, res_val = h[0]
                new_res[k] = curr_sum

                if row_idx + 1 < n:
                    # 如果 row 序列还没到头，将该 res 值对应的下一个 row 值组合入堆
                    heapq.heapreplace(h, (res_val + row[row_idx + 1], row_idx + 1, res_val))
                # else:
                #     # 如果 row 到头了，弹出堆顶
                #     heapq.heappop(h)

            # 更新 res 为合并后的前 n 个最小和
            res = new_res

        # 按照题目格式输出最小的 n 个和
        sys.stdout.write(" ".join(map(str, res)) + "\n")

if __name__ == "__main__":
    solve()
