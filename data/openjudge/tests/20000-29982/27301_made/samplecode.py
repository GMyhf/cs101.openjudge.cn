# Source: /home/ubuntu/hongfei/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def mininumRefill(plants, capacityA, capacityB):
    l, r = 0, len(plants) - 1
    Alice, Bob = capacityA, capacityB
    ans = 0
    while l <= r:
        if l == r:
            if Alice >= plants[l] or Bob >= plants[r]:
                break

            Alice = capacityA
            ans += 1
            if Alice >= plants[l]:
                break
            ans -= 1

            Bob = capacityB
            ans += 1
            if Bob >= plants[r]:
                break

        if Alice < plants[l]:
            Alice = capacityA
            ans += 1

        if Bob < plants[r]:
            Bob = capacityB
            ans += 1

        if Alice >= plants[l]:
            Alice -= plants[l]
            l += 1
        if Bob >= plants[r]:
            Bob -= plants[r]
            r -= 1

    return ans

n, AliceRaw, BobRaw = map(int, input().split())
*plants, = map(int, input().split())
print(mininumRefill(plants, AliceRaw, BobRaw))
