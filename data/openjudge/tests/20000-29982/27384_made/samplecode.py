# 27384 候选人追踪：按时间排序逐刻推进，S 内最少票数用频次桶 + 单调指针维护，S 外最多票数单调不减，O(N + K)
import sys
def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    rec = sorted((int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(n))
    s = data[2 + 2 * n:2 + 2 * n + k]
    in_s = [False] * 314160
    for x in s:
        in_s[int(x)] = True
    cnt = [0] * 314160
    freq = [0] * (n + 2)          # freq[c]：S 中恰有 c 票的人数
    freq[0] = k
    min_s = 0                     # S 中最少票数（只增不减）
    max_other = 0                 # S 外最多票数（只增不减）；K <= 314158，S 外至少一人
    ans = 0
    last = 0
    i = 0
    while i < n:
        t = rec[i][0]
        if min_s > max_other:
            ans += t - last
        while i < n and rec[i][0] == t:
            c = rec[i][1]
            if in_s[c]:
                freq[cnt[c]] -= 1
                cnt[c] += 1
                freq[cnt[c]] += 1
                while freq[min_s] == 0:
                    min_s += 1
            else:
                cnt[c] += 1
                if cnt[c] > max_other:
                    max_other = cnt[c]
            i += 1
        last = t
    print(ans)
main()
