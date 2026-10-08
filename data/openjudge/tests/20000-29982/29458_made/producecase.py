import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def count_inversions(arr):\n    # 辅助函数：归并排序并统计逆序对\n    def merge_sort(arr):\n        if len(arr) <= 1:\n            return arr, 0\n        \n        mid = len(arr) // 2\n        left, inv_left = merge_sort(arr[:mid])  # 对左半部分排序并统计逆序对\n        right, inv_right = merge_sort(arr[mid:])  # 对右半部分排序并统计逆序对\n        \n        merged, inv_split = merge(left, right)  # 合并左右两部分并统计跨越的逆序对\n        \n        return merged, inv_left + inv_right + inv_split\n    \n    # 辅助函数：合并两个有序数组并统计跨越的逆序对\n    def merge(left, right):\n        merged = []\n        i = j = inv_count = 0\n        \n        while i < len(left) and j < len(right):\n            if left[i] <= right[j]:\n                merged.append(left[i])\n                i += 1\n            else:\n                merged.append(right[j])\n                inv_count += len(left) - i  # 左边剩余的元素都比 right[j] 大\n                j += 1\n        \n        # 添加剩余的元素\n        merged.extend(left[i:])\n        merged.extend(right[j:])\n        \n        return merged, inv_count\n    \n    # 调用归并排序\n    _, total_inversions = merge_sort(arr)\n    return total_inversions\n\n# 输入处理\nn = int(input())\narr = list(map(int, input().split()))\n\n# 输出结果\nprint(count_inversions(arr))\n'
SAMPLE_IN = '6\n2 6 3 4 5 1\n'
def generate_case(r):
    n = r.randint(1, 80); a = [r.randint(1, 10**9) for _ in range(n)]
    assert len(a) == n and all(1 <= x <= 10**9 for x in a)
    return f"{n}\n" + " ".join(map(str, a)) + "\n"

MAXN = 200000


def valid(text):
    """题面：第一行 n（n<=200000）；第二行 n 个数 a[i]，1<=a[i]<=10^9。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    head = lines[0].split()
    if len(head) != 1 or not head[0].isdigit():
        return False
    n = int(head[0])
    if not 1 <= n <= MAXN:
        return False
    toks = lines[1].split(" ")
    if len(toks) != n:
        return False
    for tok in toks:
        if not tok.isdigit() or tok[0] == "0":
            return False
        if not 1 <= int(tok) <= 10**9:
            return False
    return True


def special_case(index):
    """第 30..39 组：最小规模、满规模（受 1MB 输入限制，值域大的组 n 取 85000）、全相等、逆序（答案超 int32）。"""
    r = random.Random(294580 + index)
    k = index - 30
    if k == 0:
        a = [7]                                             # n=1，答案 0
    elif k == 1:
        a = [5, 5]                                          # 相等不算逆序
    elif k == 2:
        a = [10**9, 1]                                      # 值域端点
    elif k == 3:
        a = [r.randint(1, 10**9) for _ in range(85000)]     # 大值域满载
    elif k == 4:
        a = [r.randint(1, 999) for _ in range(MAXN)]        # n 满、大量重复
    elif k == 5:
        a = [1] * MAXN                                      # 全相等，答案 0
    elif k == 6:
        a = sorted(r.randint(1, 999) for _ in range(MAXN))  # 非降序，答案 0
    elif k == 7:
        a = sorted((r.randint(1, 999) for _ in range(MAXN)), reverse=True)  # 非增序，答案约 2e10
    elif k == 8:
        a = list(range(85000, 0, -1))                       # 严格递减，答案 n(n-1)/2
    else:
        a = sorted(r.randint(1, 10**9) for _ in range(85000))
        for _ in range(3000):                               # 近乎有序
            i, j = r.randrange(85000), r.randrange(85000)
            a[i], a[j] = a[j], a[i]
    return f"{len(a)}\n" + " ".join(map(str, a)) + "\n"


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(40):
            if index == 0: content = SAMPLE_IN
            elif index >= 30: content = special_case(index)
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(29458 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content) and content not in seen[1:], index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
