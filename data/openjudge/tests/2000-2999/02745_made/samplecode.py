# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2745: 显示器
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02745/
# License: not declared; no license is inferred.
# 2021fall-cs101, 2000017793, 高骞
while True:
    s,n = input().split()
    if {s,n} == {'0'}:
        break
    else:
        s = int(s)
        a = ' '*(s+2)
        b = ' '+'-'*s+' '
        c = '|'+' '*(s+1)
        d = ' '*(s+1)+'|'
        e = '|'+' '*s+'|'
        dic = {'1':[a,d,a,d,a],'2':[b,d,b,c,b],'3':[b,d,b,d,b],'4':[a,e,b,d,a],'5':[b,c,b,d,b],
        '6':[b,c,b,e,b],'7':[b,d,a,d,a],'8':[b,e,b,e,b],'9':[b,e,b,d,b],'0':[b,e,a,e,b]}
        lis_1,lis_2,lis_3,lis_4,lis_5 = [],[],[],[],[]
        for i in range(len(n)):
            lis = dic[n[i]]
            lis_1.append(lis[0])
            lis_2.append(lis[1])
            lis_3.append(lis[2])
            lis_4.append(lis[3])
            lis_5.append(lis[4])
        lis_0 = [' '.join(lis_1),' '.join(lis_2),' '.join(lis_3),' '.join(lis_4),' '.join(lis_5)]
        for i in range(2*s+3):
            if i == 0:
                print(lis_0[0])
            elif i < s+1:
                print(lis_0[1])
            elif i == s+1:
                print(lis_0[2])
            elif i < 2*s+2:
                print(lis_0[3])
            else:
                print(lis_0[4])
        print()
