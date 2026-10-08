# External reference: http://cs101.openjudge.cn/practice/02424/statistics/
# Accepted submission: 44298654
# Source: http://cs101.openjudge.cn/practice/solution/44298654/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 参考解（审计重写）：原外部 AC 提交 44298654 在释放桌子时会把同一张桌子反复计入空闲数
# （每次都从 flag 位置重新扫描已释放的桌子），弱数据下侥幸通过，这里改为按桌型维护释放时刻小根堆。
import sys, heapq

def main():
    data = sys.stdin.read().split()
    pos = 0; out = []
    while pos + 2 < len(data):
        a, b, c = int(data[pos]), int(data[pos + 1]), int(data[pos + 2]); pos += 3
        if a == 0 and b == 0 and c == 0:
            break
        heaps = [[0] * a, [0] * b, [0] * c]
        ans = 0
        while data[pos] != "#":
            hh, mm = data[pos].split(":"); n = int(data[pos + 1]); pos += 2
            t = int(hh) * 60 + int(mm)
            h = heaps[(n - 1) // 2]
            seat = max(t, h[0])
            if seat - t <= 30:  # 等待不超过半小时就留下
                heapq.heapreplace(h, seat + 30)
                ans += n
        pos += 1
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")

main()
