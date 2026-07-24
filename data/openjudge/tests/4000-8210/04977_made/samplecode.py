# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def max_increasing_subsequence(a):
    n = len(a)
    dpu = [1] * n
    for i in range(1, n):
        for j in range(i):
            if a[i] > a[j]:
                dpu[i] = max(dpu[i], dpu[j] + 1)
    return max(dpu)

def max_decreasing_subsequence(a):
    n = len(a)
    dpd = [1] * n
    for i in range(1, n):
        for j in range(i):
            if a[i] < a[j]:
                dpd[i] = max(dpd[i], dpd[j] + 1)
    return max(dpd)

def main():
    k = int(input())
    while k:
        k -= 1
        n = int(input())
        a = list(map(int, input().split()))
        mxu = max_increasing_subsequence(a)
        mxd = max_decreasing_subsequence(a)
        print(max(mxu, mxd))

if __name__ == "__main__":
    main()
