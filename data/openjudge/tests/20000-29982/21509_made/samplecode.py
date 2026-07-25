# Source: /home/ubuntu/hongfei/2024spring-cs201/2024spring_dsa_problems.md
import heapq
import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    lo = []  # max-heap: store negative values
    hi = []  # min-heap
    
    result = []
    
    for i, num in enumerate(A):
        # Push to lo first
        heapq.heappush(lo, -num)
        
        # Move the largest in lo to hi to maintain order
        heapq.heappush(hi, -heapq.heappop(lo))
        
        # If hi has more elements, move smallest back to lo
        if len(hi) > len(lo):
            heapq.heappush(lo, -heapq.heappop(hi))
        
        # After processing odd number of elements (1st, 3rd, 5th, ...)
        if i % 2 == 0:  # 0-indexed: i=0 -> 1 element, i=2 -> 3 elements, etc.
            median = -lo[0]
            result.append(str(median))
    
    print("\n".join(result))

if __name__ == "__main__":
    main()
