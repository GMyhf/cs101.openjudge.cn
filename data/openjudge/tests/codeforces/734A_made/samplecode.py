# Written for this repository from the public problem statement; no external submission used.
# 734A Anton and Danik —— 数 'A' 的个数，其余都是 'D'，比大小（相等输出 Friendship）。
import sys

data = sys.stdin.read().split()
games = data[1]
anton = games.count("A")
danik = len(games) - anton
print("Anton" if anton > danik else "Danik" if danik > anton else "Friendship")
