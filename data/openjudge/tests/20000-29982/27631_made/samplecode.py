# External reference: http://cs101.openjudge.cn/practice/27631/statistics/
# Accepted submission: 52735644
# Source: http://cs101.openjudge.cn/practice/solution/52735644/
# License: not declared on the submission page; no license is inferred.

def solve():
    import sys
    input = sys.stdin.read().split()
    ptr = 0
    T = int(input[ptr])
    ptr += 1
    coins = [1,2,5]
    for _ in range(T):
        n = int(input[ptr])
        ptr +=1
        w = list(map(int,input[ptr:ptr+n]))
        ptr +=n
        # 检查是否全是10倍数
        bad = False
        vs = []
        for num in w:
            if num%10 !=0:
                bad=True
                break
            vs.append(num//10)
        if bad:
            print(-1)
            continue
        # 求所有余数 r = v%10
        rems = set()
        maxv = max(vs)
        for v in vs:
            rems.add(v%10)
        rems = list(rems)
        INF = 10**9
        min_cnt = INF
        # 枚举 x1(1元),x2(2元),x5(5元)
        # x1<=9, x2<=4, x5<=1
        for x1 in range(10):
            for x2 in range(5):
                for x5 in range(2):
                    ok=True
                    for r in rems:
                        flag=False
                        # 能否用<=x1个1,<=x2个2,<=x5个5凑r
                        for c5 in range(0,min(x5, r//5)+1):
                            left = r - c5*5
                            for c2 in range(0,min(x2, left//2)+1):
                                c1 = left - c2*2
                                if 0<=c1<=x1:
                                    flag=True
                                    break
                            if flag:break
                        if not flag:
                            ok=False
                            break
                    if not ok:
                        continue
                    # 计算需要多少张10元(d)
                    max_r_sum = x1 + 2*x2 +5*x5
                    d_need = 0
                    for v in vs:
                        base = v - (v%10)
                        if base > max_r_sum:
                            nd = (base - max_r_sum +9)//10
                            if nd>d_need:
                                d_need=nd
                    total = x1+x2+x5+d_need
                    if total<min_cnt:
                        min_cnt=total
        print(min_cnt)

if __name__=="__main__":
    solve()
