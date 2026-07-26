# T-003 参考实现：人提供的平台 Accepted 版本（2026-07-26 替换）
n=int(input())
for _ in range(n):
    s1,s2=input().split()
    pos=[]
    start=0
    while True:
        po=s1.find(s2,start)
        if po==-1:
            break
        pos.append(po)
        start=po+1
    if pos:
        for po in pos:
            print(po,end=' ')
        print('')
    else:
        print('no')
