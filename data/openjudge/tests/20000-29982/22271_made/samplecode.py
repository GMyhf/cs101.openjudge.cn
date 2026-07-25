# Source: /home/ubuntu/hongfei/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import sys
from collections import Counter

def main():
    # 读取输入
    input_data = sys.stdin.read().strip().split('\n')
    N = int(input_data[0])  # 树的总数
    tree_names = input_data[1:]  # 每棵树的种类名称

    # 统计每种树的数量
    tree_counter = Counter(tree_names)

    # 按字典序排序
    sorted_trees = sorted(tree_counter.items())

    # 输出结果
    for tree, count in sorted_trees:
        percentage = (count / N) * 100
        print(f"{tree} {percentage:.4f}%")

if __name__ == "__main__":
    main()
