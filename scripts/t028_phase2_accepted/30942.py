# External reference: http://cs101.openjudge.cn/practice/30942/statistics/
# Accepted submission: 52724323
# Source: http://cs101.openjudge.cn/practice/solution/52724323/
# License: not declared on the submission page; no license is inferred.

def main():
    text = input().strip()
    k = int(input())
    seen = {'F' : 0, 'T' : 0}
    l = {'F' : 0, 'T' : 0}
    ans = 0
    for i, ch in enumerate(text):
        seen[ch] += 1
        while seen[ch] > k:
            if text[l[ch]] == ch:
                seen[ch] -= 1
            l[ch] = l[ch] + 1
        min_l = min(l.values())
        ans = max(ans, i - min_l + 1)
    print(ans)
    return
if __name__ == '__main__':
    main()
