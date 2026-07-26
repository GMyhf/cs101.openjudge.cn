# T-003 参考实现：人提供的平台 Accepted 版本（2026-07-26 替换）
s=input().split('+')
a=[]
for k in s:
    a.append(list(k.split('n^')))
n=len(a)
max_a=float('-inf')
for i in range(n):
    if a[i][0]!='0':
        max_a=max(max_a,int(a[i][1]))
print(f'n^{max_a}')
