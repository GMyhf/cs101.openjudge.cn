# External reference: /practice/29657/statistics/
# Accepted submission: 52733740
# Source: http://cs101.openjudge.cn/practice/solution/52733740/
# License: not declared on the submission page; no license is inferred.

import bisect

def main():
    import sys
    input = sys.stdin.read().split()
    ptr = 0
    n1 = int(input[ptr])
    n2 = int(input[ptr+1])
    n3 = int(input[ptr+2])
    K = int(input[ptr+3])
    ptr +=4
    
    A = list(map(int, input[ptr:ptr+n1]))
    ptr +=n1
    B = list(map(int, input[ptr:ptr+n2]))
    ptr +=n2
    C = list(map(int, input[ptr:ptr+n3]))
    ptr +=n3
    
    A.sort()
    B.sort()
    C.sort()
    
    ans = 0
    for b in B:
        # 找 a < b 且 b - a <= K
        left = b - K
        l = bisect.bisect_left(A, left)
        r = bisect.bisect_left(A, b)
        cntA = r - l
        
        # 找 c > b 且 c - b <= K
        lo = b + 1
        hi = b + K
        L = bisect.bisect_right(C, lo-1)
        R = bisect.bisect_right(C, hi)
        cntC = R - L
        
        ans += cntA * cntC
    print(ans)

if __name__ == "__main__":
    main()