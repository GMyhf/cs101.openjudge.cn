import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\nfrom functools import lru_cache\n\ndef can_player1_win(nums):\n    n = len(nums)\n    \n    @lru_cache(maxsize=None)\n    def diff(i, j):\n        if i == j:\n            return nums[i]\n        return max(nums[i] - diff(i + 1, j), nums[j] - diff(i, j - 1))\n    \n    return diff(0, n - 1) >= 0\n\n# 主程序读取输入\ninput = sys.stdin.read\ndata = input().split()\n\nt = int(data[0])\nindex = 1\nresults = []\n\nfor _ in range(t):\n    m = int(data[index])\n    index += 1\n    nums = list(map(int, data[index:index + m]))\n    index += m\n    results.append("true" if can_player1_win(nums) else "false")\n\n# 输出结果\nfor res in results:\n    print(res)\n'
SAMPLE_IN = '7\n3 1 5 2\n4 1 5 233 7\n5 242 353 531 22 231\n8 231 343 63 543 54 332 541 674\n3 423 552 653\n11 231 343 63 543 54 332 541 674 423 552 653\n6 1 1 1 1 1 1\n'
def generate_case(r):
    rows = []
    for _ in range(r.randint(2, 12)):
        m = r.randint(1, 20); rows.append([r.randint(0, 1000) for _ in range(m)])
    assert all(1 <= len(a) <= 20 and all(0 <= x <= 10**7 for x in a) for a in rows)
    return str(len(rows)) + "\n" + "\n".join(f"{len(a)} " + " ".join(map(str, a)) for a in rows) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(28970 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
