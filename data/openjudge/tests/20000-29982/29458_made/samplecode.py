# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def count_inversions(arr):
    # 辅助函数：归并排序并统计逆序对
    def merge_sort(arr):
        if len(arr) <= 1:
            return arr, 0
        
        mid = len(arr) // 2
        left, inv_left = merge_sort(arr[:mid])  # 对左半部分排序并统计逆序对
        right, inv_right = merge_sort(arr[mid:])  # 对右半部分排序并统计逆序对
        
        merged, inv_split = merge(left, right)  # 合并左右两部分并统计跨越的逆序对
        
        return merged, inv_left + inv_right + inv_split
    
    # 辅助函数：合并两个有序数组并统计跨越的逆序对
    def merge(left, right):
        merged = []
        i = j = inv_count = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                inv_count += len(left) - i  # 左边剩余的元素都比 right[j] 大
                j += 1
        
        # 添加剩余的元素
        merged.extend(left[i:])
        merged.extend(right[j:])
        
        return merged, inv_count
    
    # 调用归并排序
    _, total_inversions = merge_sort(arr)
    return total_inversions

# 输入处理
n = int(input())
arr = list(map(int, input().split()))

# 输出结果
print(count_inversions(arr))
