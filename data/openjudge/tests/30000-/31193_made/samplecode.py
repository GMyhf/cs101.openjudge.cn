import sys
from collections import Counter

def solve(text):
    lines = text.splitlines()
    word = lines[0].strip(); n = int(lines[1]); rank = int(lines[2])
    rows = lines[3:3+n]
    locations = [str(i + 1) for i, row in enumerate(rows) if word in row.split()]
    counts = Counter(token for row in rows for token in row.split())
    ordered = sorted(counts, key=lambda token: (-counts[token], token))
    frequency = counts[ordered[rank - 1]] if 1 <= rank <= len(ordered) else 0
    return (" ".join(locations) if locations else "-1") + "\n" + str(frequency) + "\n"

if __name__ == '__main__':
    sys.stdout.write(solve(sys.stdin.read()))
