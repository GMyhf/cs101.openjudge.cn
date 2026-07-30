# External reference: http://cs101.openjudge.cn/practice/04020/statistics/
# Accepted submission: 51701385
# Source: http://cs101.openjudge.cn/practice/solution/51701385/
# License: not declared on the submission page; no license is inferred.

import sys

def build_all_cards():
    suits = ["Heart", "Spade", "Diamond", "Club"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
             "Ace", "Jack", "Queen", "King"]
    all_cards = set(["Joker", "joker"])
    for s in suits:
        for r in ranks:
            all_cards.add(s + r)
    return all_cards

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    idx = 1

    ALL = build_all_cards()
    out = []

    for _ in range(n):
        seen = set(data[idx:idx+53])
        idx += 53
        missing = (ALL - seen).pop()
        out.append(missing)

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
