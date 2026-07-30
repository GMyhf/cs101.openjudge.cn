# External reference: http://cs101.openjudge.cn/practice/27371/statistics/
# Accepted submission: 51495334
# Source: http://cs101.openjudge.cn/practice/solution/51495334/
# License: not declared on the submission page; no license is inferred.

def find_chr(char):
    for i in range(5):
        try:
            j=kw_ma[i].index(char)
            return (i,j)
        except ValueError:
            pass
def srt(st):
    st_pro1=[]
    st=list(st)
    l=len(st)
    for ii in range(l):
        if st[ii]=='j':
            st[ii]='i'
    i=0
    while i<l:
        st_pro1.append(st[i])
        if i==l-1 or st[i+1]==st[i]:
            if st[i]=='x':
                st_pro1.append('q')
            else:
                st_pro1.append('x')
            i+=1
        else:
            st_pro1.append(st[i+1])
            i+=2
    l=len(st_pro1)//2
    st_pro2=[]
    for i in range(l):
        a=st_pro1[2*i]
        b=st_pro1[2*i+1]
        pa=find_chr(a)
        pb=find_chr(b)
        if pa[0]==pb[0]:
            a=kw_ma[pa[0]][(pa[1]+1)%5]
            b=kw_ma[pb[0]][(pb[1]+1)%5]
        elif pa[1]==pb[1]:
            a=kw_ma[(pa[0]+1)%5][pa[1]]
            b=kw_ma[(pb[0]+1)%5][pb[1]]
        else:
            a=kw_ma[pa[0]][pb[1]]
            b=kw_ma[pb[0]][pa[1]]
        st_pro2.append(a)
        st_pro2.append(b)
    st_pro2=''.join(st_pro2)
    return st_pro2
kw=input()
tmp=[]
for char in kw:
    if char=='j':
        char='i'
    try:
        _=tmp.index(char)
    except ValueError:
        tmp.append(char)
for i in range(ord('a'),ord('z')+1):
    char=chr(i)
    if char=='j':
        char='i'
    try:
        _=tmp.index(char)
    except ValueError:
        tmp.append(char)
kw_ma=[]
for i in range(5):
    kw_ma.append(tmp[5*i:5*(i+1)])
n=int(input())
for _ in range(n):
    stg=input()
    print(srt(stg))
