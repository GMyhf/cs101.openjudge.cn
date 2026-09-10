# Written for this repository from the public problem statement; no external submission used.
# 698A Vacations —— 三状态 DP：dp[休息/写题/运动] = 到今天为止最少休息天数。
import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    days = list(map(int, data[1:1 + n]))
    INF = float("inf")
    # 0 = 休息，1 = 写题（需要 a 的第 0 位），2 = 运动（需要 a 的第 1 位）
    rest, contest, sport = 0, INF, INF
    for value in days:
        best = min(rest, contest, sport)
        rest, contest, sport = (
            best + 1,
            min(rest, sport) if value & 1 else INF,   # 昨天不能也在写题
            min(rest, contest) if value & 2 else INF,  # 昨天不能也在运动
        )
    print(min(rest, contest, sport))


main()
