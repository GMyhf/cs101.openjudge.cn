# Source: /home/ubuntu/hongfei/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import gc
import heapq
import sys


def solve():
    # 暂时禁用垃圾回收以提升执行速度
    gc.disable()

    # 以字节流形式读取输入，速度最快
    input_bytes = sys.stdin.buffer.read().split()
    if not input_bytes:
        return

    # 快速转换为整型列表
    data = list(map(int, input_bytes))
    N = data[0]
    K = data[1]

    # 利用高速 C 切片分离 A 轮和 B 轮数据
    As = data[2::2]
    Bs = data[3::2]

    # 第一轮筛选：找出 As 中值最大的前 K 个索引
    # 使用内置的 As.__getitem__ 替代 lambda 表达式，速度极快
    if K < 1000:
        top_k = heapq.nlargest(K, range(N), key=As.__getitem__)
    else:
        top_k = sorted(range(N), key=As.__getitem__, reverse=True)[:K]

    # 第二轮筛选：在 top_k 索引中，找出使 Bs 值最大的索引
    winner_idx = max(top_k, key=Bs.__getitem__)

    # 输出 1 基准的牛编号
    print(winner_idx + 1)


if __name__ == "__main__":
    solve()
