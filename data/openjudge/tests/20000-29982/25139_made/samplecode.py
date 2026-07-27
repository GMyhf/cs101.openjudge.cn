# External reference: statistics page /practice/25139/
# Accepted submission: 52740099
# Source: http://cs101.openjudge.cn/practice/solution/52740099/
# License: not declared on the submission page; no license is inferred.

from itertools import permutations

t = int(input())

for _ in range(t):
    s1, s2, s3 = input().split()

    letters = sorted(set(s1 + s2 + s3))

    # 需要非零的字母
    lead = set()
    if len(s1) > 1:
        lead.add(s1[0])
    if len(s2) > 1:
        lead.add(s2[0])
    if len(s3) > 1:
        lead.add(s3[0])

    found = False

    def dfs(idx, mp, used):
        global found

        if idx == len(letters):
            a = int("".join(str(mp[ch]) for ch in s1))
            b = int("".join(str(mp[ch]) for ch in s2))
            c = int("".join(str(mp[ch]) for ch in s3))

            if a + b == c:
                print(f"{a}+{b}={c}")
                return True
            return False

        ch = letters[idx]

        for d in range(10):
            if d in used:
                continue

            if d == 0 and ch in lead:
                continue

            mp[ch] = d
            used.add(d)

            if dfs(idx + 1, mp, used):
                return True

            used.remove(d)
            del mp[ch]

        return False

    found = dfs(0, {}, set())

    if not found:
        print("No Solution")