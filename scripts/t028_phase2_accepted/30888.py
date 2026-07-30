# External reference: http://cs101.openjudge.cn/practice/30888/statistics/
# Accepted submission: 52723272
# Source: http://cs101.openjudge.cn/practice/solution/52723272/
# License: not declared on the submission page; no license is inferred.

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    idx = 0
    N = int(data[idx])
    B = int(data[idx+1])
    idx += 2

    scores = []
    for _ in range(N):
        d = int(data[idx])
        acc = int(data[idx+1])
        idx += 2

        # 计算每首歌的贡献值
        if acc == 100:
            s = d * 1.0
        elif 95 <= acc <= 99:
            s = d * (0.5 + acc / 200)
        elif 70 <= acc <= 94:
            s = d * (acc / 150 - 1/6)
        else:
            s = 0.0
        scores.append(s)

    # 从大到小排序
    scores.sort(reverse=True)

    # 取前 B 个
    take = min(B, N)
    total = sum(scores[:take])
    avg = total / take

    # 输出 6 位小数
    print("{0:.6f}".format(avg))

if __name__ == "__main__":
    main()
