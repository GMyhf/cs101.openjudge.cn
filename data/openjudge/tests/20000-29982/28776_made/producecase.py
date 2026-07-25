import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '"""\n直接想很难想到贪心策略，不妨逆推一下，我们先假设有了一个排列，然后看怎么换排列中大臣的顺序能得到更优的结果\n\n首先，交换第i个大臣和第j个大臣(i<j)，不会影响1~i-1中的大臣的结果和第j+1~n中的大臣的结果\n设1到i-1所有大臣的左手的乘积为x_1(包括国王)，i+1到j-1中所有大臣的左手乘积为x_2，第i个大臣右手的数为r_i,左手为l_i，第j个大臣右手的数为r_j左手为l_j。\n不交换i和j:\n第i个大臣获得金币:w_1[i] = x_1 / r_i\n第j个大臣获得金币:w_1[j] = x_1 * x_2 * l_i / r_j\nans = max(ans, w_1[i], w_1[j])\n交换i和j:\n第i个大臣获得金币:w_2[i] = x_1 * x_2 * l_j / r_i\n第j个大臣获得金币:w_2[j] = x_1 / r_j\nans = max(ans, w2[i], w2[j])\n显然w_2[i]>w_1[i], w_1[j]>w_2[j]\nans = max(ans, w_2[i],w_1[j])\n\n若w_1[j]>w_2[i](即此时要交换i和j,才能得到ans最优情况,取w_2[i]而不是w1[j]):\n化简可得l_i * r_i > l_j * r_j\n也就是说，当一个大臣左右手乘积>后面的大臣的左右手乘积时,交换这两个大臣，可以得到最大答案的最小值。\n"""\nfrom typing import List\ndef Solution(n:int, a:int, b:int, lst:List[List]) -> int:\n    lst.sort(key=lambda x: (x[0] * x[1]))\n    ans = 0\n    for i in range(n):\n        ans = max(ans, a // lst[i][1])\n        a *= lst[i][0]\n    return ans\nif __name__ == "__main__":\n    n = int(input())\n    a, b = map(int, input().split())\n    lst = []\n    for i in range(n):\n        lst.append([int(_) for _ in input().split()])\n    # 时间复杂度O(nlogn)，空间复杂度O(n)\n\n    print(Solution(n, a, b, lst))\n'
SAMPLE_IN = '3 \n1 1 \n2 3 \n7 4 \n4 6\n'
def generate_case(r):
    n = r.randint(1, 8); king_a, king_b = r.randint(1, 10), r.randint(1, 10)
    ministers = [(r.randint(1, 10), r.randint(1, 10)) for _ in range(n)]
    return f"{n}\n{king_a} {king_b}\n" + "\n".join(f"{a} {b}" for a, b in ministers) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(28776 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
