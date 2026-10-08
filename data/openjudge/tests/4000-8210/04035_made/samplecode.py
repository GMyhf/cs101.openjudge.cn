# T-004-r5（04035 重写：修正拖入空列后原列不下落的错误）
import sys
def parse(s):
    a=s.split();n=int(a[0]);p=1;cols=[]
    for x in range(5):
        c=[]
        while int(a[p]):c.append(int(a[p]));p+=1
        p+=1;cols.append(tuple(c))
    return n,tuple(cols)
def settle(cols):
    cols=[list(c) for c in cols]
    while True:
        rm=set()
        for x in range(5):
            c=cols[x]
            for y in range(len(c)-2):
                if c[y]==c[y+1]==c[y+2]:rm|={(x,y),(x,y+1),(x,y+2)}
        for y in range(7):
            for x in range(3):
                if all(len(cols[x+t])>y for t in range(3)) and cols[x][y]==cols[x+1][y]==cols[x+2][y]:
                    rm|={(x,y),(x+1,y),(x+2,y)}
        if not rm:return tuple(tuple(c) for c in cols)
        cols=[[v for y,v in enumerate(cols[x]) if (x,y) not in rm] for x in range(5)]
def domove(cols,x,y,d):
    q=x+d
    if not 0<=q<5 or y>=len(cols[x]):return None
    c=[list(t) for t in cols]
    if y<len(c[q]):
        c[x][y],c[q][y]=c[q][y],c[x][y]
    else:
        if len(c[q])>=7:return None
        v=c[x].pop(y);c[q].append(v)
    return settle(c)
def solve(n,cols,prune=True):
    fail=set();path=[]
    def dfs(b,left):
        if left==0:return all(len(c)==0 for c in b)
        if (b,left) in fail:return False
        if prune:
            cnt={}
            for c in b:
                for v in c:cnt[v]=cnt.get(v,0)+1
            if any(v<3 for v in cnt.values()):fail.add((b,left));return False
        for x in range(5):
            for y in range(len(b[x])):
                for d in (1,-1):
                    if prune:
                        q=x+d
                        if 0<=q<5 and y<len(b[q]) and (d==-1 or b[q][y]==b[x][y]):continue
                    z=domove(b,x,y,d)
                    if z is None:continue
                    path.append((x,y,d))
                    if dfs(z,left-1):return True
                    path.pop()
        fail.add((b,left));return False
    return list(path) if dfs(cols,n) else None
def fmt(r):
    return '-1\n' if r is None else ''.join(f'{x} {y} {d}\n' for x,y,d in r)
if __name__=='__main__':
    n,cols=parse(sys.stdin.read())
    print(fmt(solve(n,cols,prune='--noprune' not in sys.argv)),end='')
