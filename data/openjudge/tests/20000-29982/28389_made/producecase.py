import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '"""\nDilworth定理:\nDilworth定理表明，任何一个有限偏序集的最长反链(即最长下降子序列)的长度，\n等于将该偏序集划分为尽量少的链(即上升子序列)的最小数量。\n因此，计算序列的最长下降子序列长度，即可得出最少需要多少台测试仪。\n"""\n\nfrom bisect import bisect_left\n\ndef min_testers_needed(scores):\n    scores.reverse()  # 反转序列以找到最长下降子序列的长度\n    lis = []  # 用于存储最长上升子序列\n\n    for score in scores:\n        pos = bisect_left(lis, score)\n        if pos < len(lis):\n            lis[pos] = score\n        else:\n            lis.append(score)\n\n    return len(lis)\n\n\nN = int(input())\nscores = list(map(int, input().split()))\n\nresult = min_testers_needed(scores)\nprint(result)\n'
SAMPLE_IN = '5\n1 7 3 5 2\n'
SAMPLE_OUT = '3\n'
def generate_case(r):
    values = [r.randint(0, 10000) for _ in range(r.randint(2, 45))]
    return str(len(values)) + "\n" + " ".join(map(str, values)) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(28389 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
