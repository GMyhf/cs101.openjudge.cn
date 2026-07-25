import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def count_inversions(arr):\n    # 辅助函数：归并排序并统计逆序对\n    def merge_sort(arr):\n        if len(arr) <= 1:\n            return arr, 0\n        \n        mid = len(arr) // 2\n        left, inv_left = merge_sort(arr[:mid])  # 对左半部分排序并统计逆序对\n        right, inv_right = merge_sort(arr[mid:])  # 对右半部分排序并统计逆序对\n        \n        merged, inv_split = merge(left, right)  # 合并左右两部分并统计跨越的逆序对\n        \n        return merged, inv_left + inv_right + inv_split\n    \n    # 辅助函数：合并两个有序数组并统计跨越的逆序对\n    def merge(left, right):\n        merged = []\n        i = j = inv_count = 0\n        \n        while i < len(left) and j < len(right):\n            if left[i] <= right[j]:\n                merged.append(left[i])\n                i += 1\n            else:\n                merged.append(right[j])\n                inv_count += len(left) - i  # 左边剩余的元素都比 right[j] 大\n                j += 1\n        \n        # 添加剩余的元素\n        merged.extend(left[i:])\n        merged.extend(right[j:])\n        \n        return merged, inv_count\n    \n    # 调用归并排序\n    _, total_inversions = merge_sort(arr)\n    return total_inversions\n\n# 输入处理\nn = int(input())\narr = list(map(int, input().split()))\n\n# 输出结果\nprint(count_inversions(arr))\n'
SAMPLE_IN = '6\n2 6 3 4 5 1\n'
def generate_case(r):
    n = r.randint(1, 80); a = [r.randint(1, 10**9) for _ in range(n)]
    assert len(a) == n and all(1 <= x <= 10**9 for x in a)
    return f"{n}\n" + " ".join(map(str, a)) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(29458 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
