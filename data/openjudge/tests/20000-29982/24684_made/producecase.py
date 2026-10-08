import random, re, subprocess, sys, tempfile
from pathlib import Path
REFERENCE_SOURCE = "from collections import defaultdict\n\n# 读取输入并转换成整数列表\nvotes = list(map(int, input().split()))\n\n# 使用字典统计每个选项的票数\nvote_counts = defaultdict(int)\nfor vote in votes:\n    vote_counts[vote] += 1\n\n# 找出得票最多的票数\nmax_votes = max(vote_counts.values())\n\n# 按编号顺序收集得票最多的选项\nwinners = sorted([item for item in vote_counts.items() if item[1] == max_votes])\n\n# 输出得票最多的选项，如果有多个则并列输出\nprint(' '.join(str(winner[0]) for winner in winners))\n\n"
SAMPLE_IN = '1 10 2 3 3 10\n'
SAMPLE_OUT = '3 10\n'


def valid(text):
    """题面：只有一行，若干正整数；个数不超过 100,000，最多 100 个不同选项，编号不超过 100,000。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    toks = text[:-1].split(" ")
    if not 1 <= len(toks) <= 100000:
        return False
    if not all(re.fullmatch(r"[1-9]\d*", t) and int(t) <= 100000 for t in toks):
        return False
    return len(set(toks)) <= 100


def old_case(r):
    votes = [r.randint(1, 100000) for _ in range(r.randint(5, 60))]
    return " ".join(map(str, votes)) + "\n"


def line(v):
    return " ".join(map(str, v)) + "\n"


def build_cases():
    cases, seen = [SAMPLE_IN], [SAMPLE_IN]
    for index in range(1, 8):                          # 原随机小数据保留前 7 组（多为全部并列）
        for attempt in range(100):
            content = old_case(random.Random(24684 + index + attempt * 1000))
            if content not in seen: break
        seen.append(content); cases.append(content)
    r = random.Random(246840)
    N = 100000
    cases.append(line([100000]))                        # 只有 1 票
    cases.append(line([7] * 50))                        # 全投同一项
    cases.append(line([9, 10, 100, 2, 100000, 10, 9, 100, 2, 100000]))   # 并列，按数值而非字典序
    ids = r.sample(range(1, 100001), 98) + [1, 100000]
    v = [r.choice(ids) for _ in range(N - 1)] + [ids[0]]
    cases.append(line(v))                               # 10^5 票，100 个选项随机
    v = [x for x in ids for _ in range(N // 100)]; r.shuffle(v)
    cases.append(line(v))                               # 10^5 票，100 项全部并列
    v = [r.choice(ids) for _ in range(N - 3000)] + [100000] * 3000; r.shuffle(v)
    cases.append(line(v))                               # 编号 100000 唯一最多
    v = [r.choice(ids[:98]) for _ in range(N - 5000)] + [1] * 2500 + [100000] * 2500; r.shuffle(v)
    cases.append(line(v))                               # 1 与 100000 并列第一
    small = [r.randint(1, 20) for _ in range(100)]
    v = [r.choice(small) for _ in range(N)]
    cases.append(line(v))                               # 选项少、票数多
    tied = [3, 25, 250, 99999]
    v = [x for x in tied for _ in range(20000)] + [r.choice(range(1000, 1050)) for _ in range(N - 80000)]; r.shuffle(v)
    cases.append(line(v))                               # 四项并列，含不同位数
    v = sorted(r.choice(ids) for _ in range(N))
    cases.append(line(v))                               # 有序输入
    v = [r.choice(ids[:2]) for _ in range(N)]
    cases.append(line(v))                               # 只有两个选项
    v = [x for x in ids[:99] for _ in range(999)] + [ids[99]] * 1000; r.shuffle(v)
    cases.append(line(v))                               # 100 项中唯一一项多 1 票
    return cases


def main():
    cases = build_cases()
    assert len(cases) == 20 and len(set(cases)) == 20 and all(valid(c) for c in cases)
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        for index, content in enumerate(cases):
            result = subprocess.run([sys.executable, handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            if index == 0: assert result.stdout == SAMPLE_OUT
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()
