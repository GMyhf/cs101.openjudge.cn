# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
from collections import deque


n = int(input())
queues = [deque() for _ in range(9)]
cards = deque(list(input().split()))

while cards:
    card = cards.popleft()
    queues[int(card[1])-1].append(card)

qs = {'A': deque(), 'B': deque(), 'C': deque(), 'D': deque()}
for i in range(9):
    tmp = []
    while queues[i]:
        card = queues[i].popleft()
        qs[card[0]].append(card)
        tmp.append(card)
    print(f'Queue{i+1}:'+' '.join(tmp))

result = []
for char in qs.keys():
    tmp = []
    while qs[char]:
        card = qs[char].popleft()
        result.append(card)
        tmp.append(card)
    print(f'Queue{char}:' + ' '.join(tmp))
print(*result)
