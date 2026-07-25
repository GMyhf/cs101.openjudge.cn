import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\n\n# 增加递归深度，防止深层搜索报错\nsys.setrecursionlimit(3000)\n\n\ndef dfs(count, last_val, current_R, current_dp, m, k, n):\n    """\n    count: 当前已选面值数量\n    last_val: 上一个选定的面值\n    current_R: 当前集合能连续覆盖的最大值 1..current_R\n    current_dp: 当前的DP表，current_dp[i] 表示凑成 i 所需的最少票数\n    """\n\n    # 剪枝：如果当前覆盖范围已经超过 n，说明不仅覆盖了 1..n，还覆盖了 n+1，不符合"恰好"\n    if current_R > n:\n        return 0\n\n    # 如果选够了 m 张票\n    if count == m:\n        # 检查是否恰好覆盖到 n (即 1..n 可达，n+1 不可达)\n        return 1 if current_R == n else 0\n\n    total_solutions = 0\n\n    # 确定下一个面值的搜索范围\n    # 下一个面值 v 必须满足：\n    # 1. v > last_val (保持递增，避免重复)\n    # 2. v <= current_R + 1 (保证连续性，否则 R+1 无法构成)\n    # 3. v <= n (因为如果 v >= n+1，一旦选中，R 至少会延伸到 n+1，导致 R > n 失败)\n\n    start_node = last_val + 1\n    end_node = min(current_R + 1, n)\n\n    for v in range(start_node, end_node + 1):\n        # 复制并更新 DP 表\n        # 由于只需要判断是否覆盖到 n，DP 数组大小只需维护到 n+1\n        new_dp = current_dp[:]\n\n        # 完全背包方式更新\n        # 只需要更新到 n + 1 即可，超过的部分对于判断"恰好为n"没有帮助\n        for j in range(v, n + 2):\n            if new_dp[j - v] < k:\n                if new_dp[j - v] + 1 < new_dp[j]:\n                    new_dp[j] = new_dp[j - v] + 1\n\n        # 计算新的连续覆盖范围\n        new_R = current_R\n        # 尝试向后延伸 R\n        while new_R < n + 1 and new_dp[new_R + 1] <= k:\n            new_R += 1\n\n        # 如果新范围超过 n，剪枝\n        if new_R > n:\n            continue\n\n        # 递归搜索\n        total_solutions += dfs(count + 1, v, new_R, new_dp, m, k, n)\n\n    return total_solutions\n\n\ndef solve():\n    # 读取所有输入\n    input_data = sys.stdin.read().split()\n    iterator = iter(input_data)\n    num_cases = int(next(iterator))\n\n    for _ in range(num_cases):\n        m = int(next(iterator))\n        k = int(next(iterator))\n        n = int(next(iterator))\n\n\n        # 边界情况处理\n        if m <= 0:\n            print(0)\n            continue\n\n        # 初始化 DP 数组\n        # 大小为 n + 2，用于检查 0..n+1\n        # 初始化为大数（表示不可达）\n        dp = [10000] * (n + 2)\n        dp[0] = 0\n\n        # 初始集合只有 {1}\n        # 计算 {1} 能构成的范围\n        # 能构成 x 需要 x 张票，只要 x <= k\n        limit_with_1 = min(k, n + 1)\n        for i in range(1, limit_with_1 + 1):\n            dp[i] = i\n\n        current_R = limit_with_1\n\n        # 此时如果 k >= n + 1，说明仅用 {1} 就能覆盖到 n+1，\n        # 无论后面加什么面值，范围都至少是 n+1，因此不可能"恰好为 n"\n        if current_R > n:\n            print(0)\n            continue\n\n        # 如果只需要 1 种面值\n        if m == 1:\n            print(1 if current_R == n else 0)\n            continue\n\n        # 开始 DFS\n        # 初始 count=1 (已选{1}), last_val=1\n        ans = dfs(1, 1, current_R, dp, m, k, n)\n        print(ans)\n\n\nif __name__ == \'__main__\':\n    solve()\n'
SAMPLE_IN = '4\n3 2 5\n3 2 6\n3 2 8\n3 2 9\n'
SAMPLE_OUT = '0\n3\n1\n0\n'
def generate_case(r):
    rows = [(r.randint(1, 5), r.randint(1, 3), r.randint(1, 20)) for _ in range(r.randint(2, 8))]
    return str(len(rows)) + "\n" + "\n".join(f"{m} {k} {n}" for m, k, n in rows) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(28702 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
