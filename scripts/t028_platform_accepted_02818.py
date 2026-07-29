# External reference: statistics page /practice/02818/
# Accepted submission: 46311221
# Source: http://cs101.openjudge.cn/practice/solution/46311221/
# License: not declared on the submission page; no license is inferred.

def move(st, t, a):
    for i in range(t):
        st = a[st]
    return st


# 计算周期，即加密多少次后导致的效果是相同的
def find_cir(a, n):
    ret = []    # 保存每个位置的周期，即循环节
    for i in range(n):
        x = a[i]
        cnt = 1
        while (x != i):
            x = a[x]
            cnt += 1
        ret.append(cnt)
    return ret


while (1):
    n = int(input())
    if (n == 0):
        break
    a = list(map(int, input().split()))
    for i in range(n):
        a[i] -= 1
    cir = find_cir(a, n)

    while (1):
        st = input().split(' ', 1)
        k = int(st[0])
        if (k == 0):
            break
        st = list(st[1])
        while (len(st) < n):
            st.append(' ')
        ans = [''] * n
        for i in range(n):
            # 取模省略了之前的多次不必要计算
            ans[move(i, k % cir[i], a)] = st[i]
        print(''.join(ans))
    print()
