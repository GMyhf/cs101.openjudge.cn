"""20018 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 20018
SAMPLE_IN = '5\n1\n5\n10\n7\n6\n'
SAMPLE_OUT = '7\n'
REFERENCE_SOURCE = 'import sys\nsys.setrecursionlimit(1000000)\n\ndef merge_sort(arr):\n    n = len(arr)\n    if n <= 1:\n        return arr, 0\n\n    mid = n // 2\n    left, cnt1 = merge_sort(arr[:mid])\n    right, cnt2 = merge_sort(arr[mid:])\n\n    i = j = 0\n    merged = []\n    cnt = cnt1 + cnt2\n\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            merged.append(left[i])\n            i += 1\n        else:\n            merged.append(right[j])\n            cnt += len(left) - i\n            j += 1\n\n    merged.extend(left[i:])\n    merged.extend(right[j:])\n\n    return merged, cnt\n\n\ndef main():\n    input = sys.stdin.readline\n    n = int(input())\n    v = [int(input()) for _ in range(n)]\n\n    # 转成负数，把 v[i] < v[j] 转成逆序对\n    arr = [-x for x in v]\n\n    _, ans = merge_sort(arr)\n    print(ans)\n\n\nif __name__ == "__main__":\n    main()\n'

def g20018(r):
    kind=r.random()
    n=r.randint(2,300) if kind<0.58 else (r.randint(1000,3000) if kind<0.84 else r.randint(99000,100000))
    wide=r.random()<0.5
    hi=1000 if (n>=99000 or not wide) else 10**9      # 小值域保留并列（不算赶超）的覆盖；贴上界那组也用小值域压体积
    return str(n)+"\n"+"\n".join(str(r.randint(0,hi)) for _ in range(n))+"\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20018(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    return cases

def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()
