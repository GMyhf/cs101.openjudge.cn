# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 2092: Grandpa is Famous
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02092/
# License: not declared; no license is inferred.
import sys
while True:
    n, m = map(int, input().split())
    if n == 0 and m == 0:
        break

    count = [0] * 10001
    for _ in range(n):
        for player in map(int, input().split()):
            count[player] += 1

    max_count = max(count)
    second_max_count = max(x for x in count if x != max_count)

    for player, player_count in enumerate(count):
        if player_count == second_max_count:
            print(player, end=' ')
    print()
