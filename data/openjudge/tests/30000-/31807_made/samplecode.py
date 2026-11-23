"""本仓库自写参考解；原题：dsa.openjudge.cn/2025final/E/。批量合并同权叶子。"""
import heapq
import sys


def solve(text):
    a = list(map(int, text.split()))
    heap = [(a[i], a[i+1]) for i in range(1, len(a), 2)]
    heapq.heapify(heap)
    answer = 0
    while heap:
        w, count = heapq.heappop(heap)
        while heap and heap[0][0] == w:
            count += heapq.heappop(heap)[1]
        pairs, odd = divmod(count, 2)
        if pairs:
            answer += 2 * w * pairs
            heapq.heappush(heap, (2 * w, pairs))
        if odd:
            if not heap:
                break
            v, c = heapq.heappop(heap)
            if c > 1:
                heapq.heappush(heap, (v, c-1))
            answer += w + v
            heapq.heappush(heap, (w + v, 1))
    return str(answer) + '\n'


if __name__ == '__main__':
    print(solve(sys.stdin.read()), end='')
