# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
import sys
sys.setrecursionlimit(1000000)

def merge_sort(arr):
    n = len(arr)
    if n <= 1:
        return arr, 0

    mid = n // 2
    left, cnt1 = merge_sort(arr[:mid])
    right, cnt2 = merge_sort(arr[mid:])

    i = j = 0
    merged = []
    cnt = cnt1 + cnt2

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            cnt += len(left) - i
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged, cnt


def main():
    input = sys.stdin.readline
    n = int(input())
    v = [int(input()) for _ in range(n)]

    # 转成负数，把 v[i] < v[j] 转成逆序对
    arr = [-x for x in v]

    _, ans = merge_sort(arr)
    print(ans)


if __name__ == "__main__":
    main()
