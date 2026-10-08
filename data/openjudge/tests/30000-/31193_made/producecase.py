import random
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
SAMPLE = "I\n4\n3\nI am a student .\nI live in Beijing and I love Bejing\nI also love travelling, life in there\nBeijing is beautiful\n"


def valid(text):
    """题面契约：第一行查询词 W（一个单词）；第二行行数 N；第三行频次排名 R；
    其后恰 N 行文本，单词之间以空格隔开；排名 R 必须对应一个真实存在的词（1 <= R <= 不同单词数）。"""
    if not text.endswith("\n") or "\r" in text or "\t" in text:
        return False
    lines = text[:-1].split("\n")
    if len(lines) < 3:
        return False
    word = lines[0]
    if not word or " " in word:
        return False
    def count(x):
        return int(x) if x.isdigit() and x[0] != "0" else None
    n, rank = count(lines[1]), count(lines[2])
    if n is None or rank is None or len(lines) != n + 3:
        return False
    vocab = set()
    for row in lines[3:]:
        tokens = row.split(" ")
        if not row or any(t == "" for t in tokens):
            return False
        vocab.update(tokens)
    return 1 <= rank <= len(vocab)


BASE = ["I", "i", "am", "a", "A", "student", ".", ",", "live", "in", "Beijing", "Bejing", "and", "love",
        "also", "travelling,", "life", "there", "is", "beautiful", "the", "The", "of", "to", "inn", "lin"]


def build(rng, n, words_per_line, vocab, weights=None, query=None, absent=False, rank=None):
    rows = [" ".join(rng.choices(vocab, weights=weights, k=rng.randint(*words_per_line))) for _ in range(n)]
    present = sorted({t for r in rows for t in r.split()})
    if query is None:
        if absent:
            cands = [w for w in BASE + ["missing", "Beijing.", "lov", "loves"] if w not in present]
            query = rng.choice(cands)
        else:
            query = rng.choice(present)
    if rank is None:
        rank = rng.randint(1, len(present))
    rank = max(1, min(rank, len(present)))
    return f"{query}\n{n}\n{rank}\n" + "\n".join(rows) + "\n"


def generate(i):
    if i == 0:
        return SAMPLE
    rng = random.Random(3119300 + i)
    if i <= 20:
        # 小规模：大小写敏感、子串陷阱（in / inn / lin）、同一行重复出现、排名 1 与末名
        vocab = rng.sample(BASE, rng.randint(4, len(BASE)))
        rank = 1 if i % 5 == 1 else (10**9 if i % 5 == 2 else None)
        return build(rng, rng.randint(1, 10), (1, 8), vocab, absent=(i % 4 == 0), rank=rank)
    if i <= 28:
        vocab = BASE + [f"w{k}" for k in range(rng.randint(10, 200))]
        weights = [1 / (k + 1) for k in range(len(vocab))]
        return build(rng, rng.randint(50, 600), (1, 15), vocab, weights, absent=(i % 4 == 0))
    if i <= 34:
        # 大规模：约 5000 行、Zipf 分布词频
        vocab = BASE + [f"w{k}" for k in range(3000)]
        weights = [1 / (k + 1) for k in range(len(vocab))]
        rank = {29: 1, 30: 10**9}.get(i)
        return build(rng, 5000, (1, 15), vocab, weights, absent=(i == 32), rank=rank)
    if i == 35:
        return "x\n1\n1\nx\n"
    if i == 36:
        return "in\n3\n2\nBeijing living inn\nlin in in in\nmain\n"
    if i == 37:
        # 查询词出现在每一行
        rows = [" ".join(["key"] + rng.choices(BASE, k=rng.randint(0, 10))) for _ in range(3000)]
        return f"key\n3000\n3\n" + "\n".join(rows) + "\n"
    if i == 38:
        # 所有词互不相同，排名取末名
        words = [f"u{k}" for k in range(20000)]
        rows = [" ".join(words[k:k + 10]) for k in range(0, 20000, 10)]
        return f"u19999\n{len(rows)}\n20000\n" + "\n".join(rows) + "\n"
    if i == 39:
        # 大小写区分：Love 不等于 love
        return "Love\n3\n2\nlove love Love\nLOVE love\nlove\n"
    raise ValueError(i)


def main():
    for i in range(40):
        case = generate(i)
        out = subprocess.run(['python3', str(ROOT / 'samplecode.py')], input=case, text=True, capture_output=True, check=True).stdout
        (ROOT / 'data' / f'{i}.in').write_text(case)
        (ROOT / 'data' / f'{i}.out').write_text(out)


if __name__ == "__main__":
    main()
