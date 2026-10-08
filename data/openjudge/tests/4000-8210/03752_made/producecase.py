import random,subprocess,tempfile
from collections import deque
from pathlib import Path
REFERENCE_SOURCE='import sys\nfrom collections import deque\na=sys.stdin.read().split(); r,c=map(int,a[:2]); g=a[2:]; d=[[-1]*c for _ in range(r)]\nq=deque([(0,0)]); d[0][0]=1\nwhile q:\n    x,y=q.popleft()\n    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):\n        u,v=x+dx,y+dy\n        if 0<=u<r and 0<=v<c and g[u][v]=="." and d[u][v]<0:\n            d[u][v]=d[x][y]+1; q.append((u,v))\nprint(d[-1][-1])'
SAMPLE_IN='5 5\n..###\n#....\n#.#.#\n#.#.#\n#.#..\n'


def reachable(g):
    R,C=len(g),len(g[0]);seen={(0,0)};q=deque([(0,0)])
    while q:
        x,y=q.popleft()
        for u,v in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=u<R and 0<=v<C and g[u][v]=="." and (u,v) not in seen:
                seen.add((u,v));q.append((u,v))
    return (R-1,C-1) in seen


def valid(text):
    """题面：首行 R C（1<=R,C<=40），接着 R 行每行 C 个字符（'.' 空地、'#' 障碍），
    左上角与右下角都是 '.'，且数据保证一定能从左上角走到右下角。"""
    if not text.endswith("\n"):
        return False
    lines=text[:-1].split("\n")
    head=lines[0].split(" ")
    if len(head)!=2 or not all(x.isdigit() for x in head):
        return False
    R,C=map(int,head)
    if not (1<=R<=40 and 1<=C<=40) or len(lines)!=R+1:
        return False
    g=lines[1:]
    if any(len(row)!=C or set(row)-set(".#") for row in g):
        return False
    if g[0][0]!="." or g[-1][-1]!=".":
        return False
    return reachable(g)


def perfect_maze(R,C,r):
    """在奇数格上做随机 DFS 生成树迷宫，路径长且唯一。"""
    g=[["#"]*C for _ in range(R)]
    st=[(0,0)];g[0][0]="."
    while st:
        x,y=st[-1];nb=[]
        for dx,dy in ((2,0),(-2,0),(0,2),(0,-2)):
            u,v=x+dx,y+dy
            if 0<=u<R and 0<=v<C and g[u][v]=="#": nb.append((u,v))
        if not nb: st.pop();continue
        u,v=r.choice(nb);g[(x+u)//2][(y+v)//2]=".";g[u][v]=".";st.append((u,v))
    # 偶数边长时把终点接到最近的已开通格
    i,j=R-1,C-1
    while g[i][j]=="#":
        g[i][j]="."
        if i>0 and g[i-1][j]=="#" and (j==0 or g[i][j-1]=="#"): i-=1
        elif j>0: j-=1
        else: i-=1
    return g


def snake(R,C):
    g=[["#"]*C for _ in range(R)]
    for i in range(0,R,2):
        for j in range(C): g[i][j]="."
        if i+1<R: g[i+1][C-1 if (i//2)%2==0 else 0]="."
    if R%2==0:
        for j in range(C): g[R-1][j]="."
    return g


def random_grid(R,C,dens,r):
    while True:
        g=[["#" if r.random()<dens else "." for _ in range(C)] for _ in range(R)]
        g[0][0]=".";g[-1][-1]="."
        if reachable(g): return g


def g3752(index,r):
    if index==1: g=[["."]]
    elif index==2: g=random_grid(1,40,0.0,r)
    elif index==3: g=random_grid(40,1,0.0,r)
    elif index==4: g=random_grid(40,40,0.0,r)
    elif index==5: g=snake(40,40)
    elif index==6: g=snake(39,40)
    elif index==7: g=perfect_maze(39,39,r)
    elif index==8: g=perfect_maze(40,40,r)
    elif index==9: g=perfect_maze(40,39,r)
    elif index==10: g=random_grid(1,2,0.0,r)
    elif index==11: g=random_grid(2,1,0.0,r)
    elif index<=20: g=perfect_maze(r.randint(20,40),r.randint(20,40),r)
    elif index<=30: g=random_grid(r.randint(30,40),r.randint(30,40),r.choice([0.2,0.3,0.38,0.42]),r)
    else: g=random_grid(r.randint(1,40),r.randint(1,40),r.choice([0.1,0.25,0.35]),r)
    return f"{len(g)} {len(g[0])}\n"+"".join("".join(row)+"\n" for row in g)


def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE);handle.flush()
        root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
        for index in range(40):
            if index==0: content=SAMPLE_IN
            else:
                for attempt_no in range(100):
                    content=g3752(index,random.Random(3752+index+attempt_no*1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
                seen.append(content)
            assert valid(content),index
            result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
            (root/f"{index}.in").write_text(content,encoding="utf-8")
            (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")


if __name__=="__main__":
    main()
