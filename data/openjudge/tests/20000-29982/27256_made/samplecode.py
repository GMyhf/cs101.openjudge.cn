# External reference: http://cs101.openjudge.cn/practice/27256/statistics/
# Accepted submission: 52727708
# Source: http://cs101.openjudge.cn/practice/solution/52727708/
# License: not declared on the submission page; no license is inferred.

from collections import deque
import heapq

n = int(input())
q = deque()

heap_min = []
heap_max = []

result = []
delete = set()
where = {}

size_min = 0
size_max = 0
idx = 0

def clean_min():
    while heap_min and heap_min[0][1] in delete:
        heapq.heappop(heap_min)

def clean_max():
    while heap_max and heap_max[0][1] in delete:
        heapq.heappop(heap_max)

def balance():
    global size_max, size_min

    clean_max()
    clean_min()

    if size_min > size_max + 1:
        num, idx = heapq.heappop(heap_min)
        size_min -= 1

        heapq.heappush(heap_max, (-num, idx))
        where[idx] = 'max'
        size_max += 1

    if size_max > size_min:
        num, idx = heapq.heappop(heap_max)
        size_max -= 1

        heapq.heappush(heap_min, (-num, idx))
        where[idx] = 'min'
        size_min += 1

    clean_max()
    clean_min()

for i in range(n):
    data = input()

    if data[0] == 'a':
        add, num = data.split()
        num = int(num)

        q.append((num, idx))

        clean_min()

        if not heap_min or heap_min[0][0] <= num:
            heapq.heappush(heap_min, (num, idx))
            where[idx] = 'min'
            size_min += 1

        else:
            heapq.heappush(heap_max, (-num, idx))
            where[idx] = 'max'
            size_max += 1

        idx += 1
        balance()

    elif data[0] == 'q':
        if size_max < size_min:
            result.append(heap_min[0][0])

        else:
            a = (heap_min[0][0] - heap_max[0][0])/2
            if a == int(a):
                result.append(int(a))

            else:
                result.append(a)

    elif data[0] == 'd':
        num, index = q.popleft()

        delete.add(index)

        if where[index] == 'min':
            size_min -= 1
        else:
            size_max -= 1

        balance()


for x in result:
    print(x)
