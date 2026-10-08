import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\nfrom functools import lru_cache\n\ndef can_player1_win(nums):\n    n = len(nums)\n    \n    @lru_cache(maxsize=None)\n    def diff(i, j):\n        if i == j:\n            return nums[i]\n        return max(nums[i] - diff(i + 1, j), nums[j] - diff(i, j - 1))\n    \n    return diff(0, n - 1) >= 0\n\n# 主程序读取输入\ninput = sys.stdin.read\ndata = input().split()\n\nt = int(data[0])\nindex = 1\nresults = []\n\nfor _ in range(t):\n    m = int(data[index])\n    index += 1\n    nums = list(map(int, data[index:index + m]))\n    index += m\n    results.append("true" if can_player1_win(nums) else "false")\n\n# 输出结果\nfor res in results:\n    print(res)\n'
SAMPLE_IN = '7\n3 1 5 2\n4 1 5 233 7\n5 242 353 531 22 231\n8 231 343 63 543 54 332 541 674\n3 423 552 653\n11 231 343 63 543 54 332 541 674 423 552 653\n6 1 1 1 1 1 1\n'
import re
SEED_BASE = 28970
_INT = re.compile(r'-?(0|[1-9][0-9]*)$')

def _ints(line):
    t = line.split(' ')
    if any(not _INT.match(x) for x in t): return None
    return [int(x) for x in t]

def valid(text):
    """题面：第一行组数 n（n ≤ 350），之后 n 行，每行 m 与 m 个元素，1 ≤ m ≤ 20，0 ≤ nums[i] ≤ 10^7。"""
    if not text.endswith('\n'): return False
    L = text[:-1].split('\n')
    h = _ints(L[0])
    if h is None or len(h) != 1 or not 1 <= h[0] <= 350 or len(L) != h[0] + 1: return False
    for line in L[1:]:
        a = _ints(line)
        if a is None or not 1 <= a[0] <= 20 or len(a) != a[0] + 1: return False
        if any(not 0 <= x <= 10**7 for x in a[1:]): return False
    return True

def generate_case(r):
    rows = []
    for _ in range(r.randint(2, 12)):
        m = r.randint(1, 20); rows.append([r.randint(0, 1000) for _ in range(m)])
    assert all(1 <= len(a) <= 20 and all(0 <= x <= 10**7 for x in a) for a in rows)
    return str(len(rows)) + "\n" + "\n".join(f"{len(a)} " + " ".join(map(str, a)) for a in rows) + "\n"

def _fmt(rows):
    return str(len(rows)) + "\n" + "\n".join(f"{len(a)} " + " ".join(map(str, a)) for a in rows) + "\n"

def _best(a):
    # 区间 DP：先手在 a[i..j] 上能拿到的最大总分
    n = len(a); pre = [0]
    for x in a: pre.append(pre[-1] + x)
    f = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        f[i][i] = a[i]
        for j in range(i + 1, n):
            s = pre[j + 1] - pre[i]
            f[i][j] = s - min(f[i + 1][j], f[i][j - 1])
    return 2 * f[0][n - 1] >= pre[n]

def _greedy(a):
    # 常见错解：每次取两端较大者
    i, j, s1, s2, t = 0, len(a) - 1, 0, 0, 0
    while i <= j:
        if a[i] >= a[j]: x = a[i]; i += 1
        else: x = a[j]; j -= 1
        if t == 0: s1 += x
        else: s2 += x
        t ^= 1
    return s1 >= s2

def extra_cases():
    r = random.Random(289700)
    out = []
    # 组数 n=1 的最小规模
    out.append(_fmt([[0]]))
    out.append(_fmt([[3, 7, 1]]))          # false
    # 满规模：n=350，m=20，值域到 10^7
    for k in range(3):
        rows = [[r.randint(0, 10**7) for _ in range(20)] for _ in range(350)]
        out.append(_fmt(rows))
    # n=350，m 在 1..20 间混合，含极值
    rows = []
    for _ in range(350):
        m = r.randint(1, 20); rows.append([r.choice([0, 10**7, r.randint(0, 10**7)]) for _ in range(m)])
    out.append(_fmt(rows))
    # 平局（得分相等算 true）、全 0、全相等
    rows = [[0] * m for m in range(1, 21)] + [[10**7] * m for m in range(1, 21)] + [[5, 5], [1, 2, 1, 2], [2, 1, 1, 2]]
    out.append(_fmt(rows))
    # 卡贪心：贪心与正解不同的数组
    rows = []
    while len(rows) < 350:
        m = r.randint(3, 20); a = [r.randint(0, 10**7) if r.random() < .5 else r.randint(0, 20) for _ in range(m)]
        if _greedy(a) != _best(a): rows.append(a)
    out.append(_fmt(rows))
    # 正反比例均衡：小值域随机 + 奇数长度，false 更多
    for k in range(3):
        rows = []
        want = [True, False] * 175
        for w in want:
            while True:
                m = r.randint(1, 20); a = [r.randint(0, 9) for _ in range(m)]
                if _best(a) == w: rows.append(a); break
        out.append(_fmt(rows))
    return out

def build_cases():
    seen = [SAMPLE_IN]
    cases = []
    for index in range(40):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(SEED_BASE + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content); cases.append(content)
    for content in extra_cases():
        assert content not in cases, "duplicate extra case"
        cases.append(content)
    for content in cases:
        assert valid(content), content[:80]
    return cases

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        for index, content in enumerate(build_cases()):
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
