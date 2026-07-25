# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import math


def bacteria_war(harmful: int, beneficial: int) -> int:
    hours = 0
    while harmful > 0:
        # Step 1: 有益菌消灭有害菌
        harmful = max(0, harmful - beneficial)

        # Step 2: 有害菌繁殖（在消灭之后进行）
        harmful *= 2
        harmful = min(harmful, 1_000_000)

        # Step 3: 有益菌繁殖
        beneficial = math.floor(beneficial * 1.05)

        # Step 4: 时间增加
        hours += 1
    return hours


# 主程序部分
def main():
    n = int(input())
    results = []
    for _ in range(n):
        h, b = map(int, input().split())
        results.append(bacteria_war(h, b))
    for res in results:
        print(res)


if __name__ == "__main__":
    main()

