# External reference: statistics page /practice/21517/
# Accepted submission: 52740168
# Source: http://cs101.openjudge.cn/practice/solution/52740168/
# License: not declared on the submission page; no license is inferred.

def main():
    import sys
    from collections import defaultdict
    input = sys.stdin.read().split()
    ptr = 0
    N = int(input[ptr])
    ptr += 1
    
    strs = []
    for _ in range(N):
        M = int(input[ptr])
        ptr += 1
        a = list(map(int, input[ptr:ptr+M]))
        ptr += M
        # 生成差分序列
        diff = []
        for i in range(M-1):
            diff.append(str(a[i+1] - a[i]))
        strs.append(diff)
    
    # 二分最长长度
    l = 0
    r = max(len(s) for s in strs)
    ans = 0
    
    while l <= r:
        mid = (l + r) // 2
        if mid == 0:
            ans = max(ans, 0)
            l = mid + 1
            continue
        
        cnt = defaultdict(int)
        ok = False
        
        # 处理第一个串
        s = strs[0]
        se = set()
        for i in range(len(s) - mid + 1):
            sub = ','.join(s[i:i+mid])
            se.add(sub)
        for k in se:
            cnt[k] += 1
        
        # 处理其他串
        for idx in range(1, N):
            s = strs[idx]
            se = set()
            for i in range(len(s) - mid + 1):
                sub = ','.join(s[i:i+mid])
                se.add(sub)
            for k in se:
                cnt[k] += 1
        
        # 检查是否有全部串都出现的子串
        if N in cnt.values():
            ok = True
        
        if ok:
            ans = mid
            l = mid + 1
        else:
            r = mid - 1
    
    print(ans + 1)

if __name__ == "__main__":
    main()