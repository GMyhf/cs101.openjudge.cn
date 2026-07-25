import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "from collections import defaultdict\n\n# 读取输入并转换成整数列表\nvotes = list(map(int, input().split()))\n\n# 使用字典统计每个选项的票数\nvote_counts = defaultdict(int)\nfor vote in votes:\n    vote_counts[vote] += 1\n\n# 找出得票最多的票数\nmax_votes = max(vote_counts.values())\n\n# 按编号顺序收集得票最多的选项\nwinners = sorted([item for item in vote_counts.items() if item[1] == max_votes])\n\n# 输出得票最多的选项，如果有多个则并列输出\nprint(' '.join(str(winner[0]) for winner in winners))\n\n"
SAMPLE_IN = '1 10 2 3 3 10\n'
SAMPLE_OUT = '3 10\n'
def generate_case(r):
    votes = [r.randint(1, 100000) for _ in range(r.randint(5, 60))]
    assert len(votes) <= 100000 and len(set(votes)) <= 100
    return " ".join(map(str, votes)) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(24684 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
