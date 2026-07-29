# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 2299: Ultra-QuickSort
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02299/
# License: not declared in source collection; no license is inferred.
import sys
"""
问题：分析特定排序算法，通过交换两个相邻的序列元素来处理n个不同的整数序列，直到序列按升序排序。
任务是确定需要执行多少次交换操作才能对给定的输入序列进行排序。

可以通过使用归并排序的修改版本来解决，计算在每次合并步骤中需要的交换次数。
在归并排序中，将数组分成两半，对每一半进行排序，然后将它们合并在一起。

在合并步骤中，计算需要交换的次数，因为每当从右半部分取出一个元素时，
需要交换与左半部分中剩余元素相同数量的次数。
"""
def merge_sort(lst):
    # The list is already sorted if it contains a single element.
    if len(lst) <= 1:
        return lst, 0

    # Divide the input into two halves.
    middle = len(lst) // 2
    left, inv_left = merge_sort(lst[:middle])
    right, inv_right = merge_sort(lst[middle:])

    merged, inv_merge = merge(left, right)

    # The total number of inversions is the sum of inversions in the recursion and the merge process.
    return merged, inv_left + inv_right + inv_merge

def merge(left, right):
    merged = []
    inv_count = 0
    i = j = 0

    # Merge smaller elements first.
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            inv_count += len(left) - i #left[i~mid)都比right[j]要大，他们都会与right[j]构成逆序对，将他们加入答案

    # If there are remaining elements in the left or right half, append them to the result.
    merged += left[i:]
    merged += right[j:]

    return merged, inv_count

while True:
    n = int(input())
    if n == 0:
        break

    lst = []
    for _ in range(n):
        lst.append(int(input()))

    _, inversions = merge_sort(lst)
    print(inversions)
