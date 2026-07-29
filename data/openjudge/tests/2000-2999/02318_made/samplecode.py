# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2318: TOYS
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02318/
# License: not declared; no license is inferred.
def compute_bin(toy_x, toy_y, y1, y2, partitions):
    # 二分查找找到 toy 落在哪个 bin 中
    left, right = 0, len(partitions)
    while left < right:
        mid = (left + right) // 2
        u, l = partitions[mid]
        # 计算直线 (u,y1) 到 (l,y2) 在 toy_y 高度的 x 坐标
        part_x = u + (l - u) * (y1 - toy_y) / (y1 - y2)
        if toy_x < part_x:
            right = mid
        else:
            left = mid + 1
    return left

def main():
    import sys
    input_lines = sys.stdin.read().splitlines()
    idx = 0
    output = []

    while idx < len(input_lines):
        line = input_lines[idx].strip()
        idx += 1
        if line == '0':
            break
        if not line:
            continue
        n, m, x1, y1, x2, y2 = map(int, line.split())
        partitions = []
        for _ in range(n):
            u, l = map(int, input_lines[idx].split())
            partitions.append((u, l))
            idx += 1
        toys = []
        for _ in range(m):
            x, y = map(int, input_lines[idx].split())
            toys.append((x, y))
            idx += 1

        bin_counts = [0] * (n + 1)
        for tx, ty in toys:
            bin_index = compute_bin(tx, ty, y1, y2, partitions)
            bin_counts[bin_index] += 1

        for i, count in enumerate(bin_counts):
            output.append(f"{i}: {count}")
        output.append("")  # blank line between problems

    print("\n".join(output).strip())  # strip the last blank line

if __name__ == "__main__":
    main()
