# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# 23n2300017735(夏天明BrightSummer)
def find(s, pat):
    nex = [0]
    for i, p in enumerate(pat[1:], 1):
        tmp = nex[i-1]
        while True:
            if p == pat[tmp]:
                nex.append(tmp+1)
                break
            elif tmp:
                tmp = nex[tmp-1]
            else:
                nex.append(0)
                break
    j = 0
    for i, char in enumerate(s):
        while True:
            if char == pat[j]:
                j += 1
                if j == len(pat):
                    return i
                break
            elif j:
                j -= nex[j]
            else:
                break

s, p1, p2 = input().split(',')
try:
    assert((ans := len(s)-find(s, p1)-find(s[::-1], p2[::-1])-2) >= 0)
    print(ans)
except (TypeError, AssertionError):
    print(-1)
