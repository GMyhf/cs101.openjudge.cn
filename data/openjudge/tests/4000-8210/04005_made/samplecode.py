# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def get_max_profit(a1, a2):
    la1 = 0
    ra1 = len(a1) - 1
    la2 = 0
    ra2 = len(a2) - 1
    ans_max = 0
    ans_min = 0

    while la2 <= ra2:
        if a2[la2] > a1[la1]:
            ans_max += 3
            ans_min += 1
            la1 += 1
            la2 += 1
        elif a2[ra2] > a1[ra1]:
            ans_max += 3
            ans_min += 1
            ra1 -= 1
            ra2 -= 1
        else:
            if a2[la2] < a1[ra1]:
                ans_max += 1
                ans_min += 3
            elif a2[la2] == a1[ra1]:
                ans_max += 2
                ans_min += 2

            la2 += 1
            ra1 -= 1

    return ans_max, ans_min


while True:
    n = int(input())
    if n == 0:
        break

    *C, = map(int, input().split())
    *S, = map(int, input().split())
    C.sort()
    S.sort()

    ans_max, _ = get_max_profit(C, S)
    _, ans_min = get_max_profit(S, C)

    print(ans_max, ans_min)
