# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# https://www.geeksforgeeks.org/naive-algorithm-for-pattern-searching/
# Naive Pattern Searching algorithm
def search(pat, txt):
    M = len(pat)
    N = len(txt)

    res = []
    # A loop to slide pat[] one by one */
    for i in range(N - M + 1):
    #i = 0
    #while i < N - M + 1:
        j = 0

        # For current index i, check
        # for pattern match */
        while(j < M):
            if (txt[i + j] != pat[j]):
                #i = i+j + 1
                break
            j += 1

        if (j == M):
            res.append(str(i))
            #i += M

    return res


n = int(input())
for _ in range(n):
    txt, pat = input().split()
    ans = search(pat, txt)
    if ans:
        print(' '.join(ans))
    else:
        print('no')
