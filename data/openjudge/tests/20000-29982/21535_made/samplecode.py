# Source: /home/ubuntu/hongfei/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def main():
    # Read the input
    n, w = map(int, input().split())
    P, Q = map(int, input().split())
    # The amplified skill damage
    damage = P + Q

    monsters = []
    for i in range(n):
        x, y = map(int, input().split())
        if damage >= x:
            monsters.append(y)

    # Sort monsters by the magic cost (y) in ascending order
    monsters.sort()

    # Count how many monsters we can defeat
    count = 0
    for cost in monsters:
        if w >= cost:
            w -= cost
            count += 1
        else:
            break

    print(count)


if __name__ == '__main__':
    main()

