# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
import heapq

def min_weighted_path_length(n, weights):
    heapq.heapify(weights)
    total = 0
    while len(weights) > 1:
        a = heapq.heappop(weights)
        b = heapq.heappop(weights)
        combined = a + b
        total += combined
        heapq.heappush(weights, combined)
    return total

# 读取输入
n = int(input())
weights = list(map(int, input().split()))
print(min_weighted_path_length(n, weights))
