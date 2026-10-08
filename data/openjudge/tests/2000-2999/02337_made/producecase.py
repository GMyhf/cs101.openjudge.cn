import random,subprocess,sys,tempfile
from pathlib import Path
def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    letters = "abcdefghijklmnopqrstuvwxyz"
    word = lambda a=1, b=10: "".join(r.choice(letters) for _ in range(r.randint(a, b)))
    if number == 3247: return f"{seed % 9 + 1}\n"
    if number == 1002:
        base = ["4873279", "ITS-EASY", "888-4567", "3-10-10-10"]
        rows = [r.choice(base) for _ in range(r.randint(2, 30))]
        return f"{len(rows)}\n" + "\n".join(rows) + "\n"
    if number == 2181:
        a = [r.randint(0, 1000) for _ in range(r.randint(1, 100))]
        return f"{len(a)}\n" + "\n".join(map(str, a)) + "\n"
    if number == 2936:
        a = sorted(r.sample(range(1, 9), r.randint(1, 8))); return f"{len(a)}\n" + " ".join(map(str, a)) + "\n"
    if number == 2814: return " ".join(str(r.randrange(4)) for _ in range(9)) + "\n"
    if number == 2910:
        chars = letters + letters.upper() + "0123456789*?-_"; return "".join(r.choice(chars) for _ in range(r.randint(1, 100))) + "\n"
    if number == 2940: return f"{r.randint(1,9)} {r.randint(1,9)}\n"
    if number == 1178:
        squares = [f"{chr(65+x)}{y+1}" for y in range(8) for x in range(8)]
        return "".join(r.sample(squares, r.randint(2, 12))) + "\n"
    if number == 1190: return f"{r.randint(1, 2000)}\n{r.randint(1, 7)}\n"
    if number == 2899:
        rows = [" ".join(str(r.randint(-1000, 1000)) for _ in range(5)) for _ in range(5)]
        return "\n".join(rows) + f"\n{r.randint(-2,6)} {r.randint(-2,6)}\n"
    if number == 2942: return f"{seed % 19 + 1}\n"
    if number == 2791:
        pts=set(); n=r.randint(2,8)
        while len(pts)<n: pts.add((r.randint(-20,20),r.randint(-20,20)))
        return f"{n}\n"+"\n".join(f"{x} {y}" for x,y in pts)+"\n0\n"
    if number == 2804:
        foreign=[]; rows=[]
        for _ in range(r.randint(2,15)):
            f=word(); foreign.append(f); rows.append(f"{word()} {f}")
        docs=[r.choice(foreign+[word()]) for _ in range(r.randint(2,20))]
        return "\n".join(rows)+"\n\n"+"\n".join(docs)+"\n"
    if number == 1077:
        board=list("12345678x"); pos=8
        for _ in range(r.randint(0,30)):
            y,x=divmod(pos,3); choices=[q for q in (pos-3,pos+3,pos-1,pos+1) if 0<=q<9 and abs(q%3-x)+abs(q//3-y)==1]
            q=r.choice(choices);board[pos],board[q]=board[q],board[pos];pos=q
        return " ".join(board)+"\n"
    if number == 1230:
        cases=[]
        for _ in range(r.randint(1,4)):
            n=r.randint(1,20); k=r.randint(0,10); walls=[]
            for _ in range(n):
                x1,x2=sorted((r.randint(0,100),r.randint(0,100))); y=r.randint(0,100);walls.append(f"{x1} {y} {x2} {y}")
            cases.append(f"{n} {k}\n"+"\n".join(walls))
        return f"{len(cases)}\n"+"\n".join(cases)+"\n"
    if number == 1276:
        cases=[]
        for _ in range(r.randint(1,5)):
            n=r.randint(1,12); pairs=[(r.randint(1,20),r.randint(1,200)) for _ in range(n)]
            cases.append(f"{r.randint(0,3000)} {n} "+" ".join(f"{c} {v}" for c,v in pairs))
        return "\n".join(cases)+"\n"
    if number == 1481:
        w=h=r.randint(5,15); grid=[["."]*w for _ in range(h)]
        for y,x in [(2,2),(2,3),(3,2),(3,3)]: grid[y][x]="*"
        for y,x in r.sample([(2,2),(2,3),(3,2),(3,3)],r.randint(1,4)):grid[y][x]="X"
        return f"{w} {h}\n"+"\n".join("".join(x) for x in grid)+"\n0 0\n"
    if number == 2049:
        if seed % 2:
            x,y=r.randint(1,198),r.randint(1,198);return f"0 0\n{x}.5 {y}.5\n-1 -1\n"
        # The statement sample exercises walls and doors; translate it so even
        # seeds remain distinct without changing its topology.
        d=seed % 30
        return ("8 9\n"+"\n".join((f"{1+d} 1 1 3",f"{2+d} 1 1 3",f"{3+d} 1 1 3",f"{4+d} 1 1 3",
          f"{1+d} 1 0 3",f"{1+d} 2 0 3",f"{1+d} 3 0 3",f"{1+d} 4 0 3",
          f"{2+d} 1 1",f"{2+d} 2 1",f"{2+d} 3 1",f"{3+d} 1 1",f"{3+d} 2 1",f"{3+d} 3 1",
          f"{1+d} 2 0",f"{3+d} 3 0",f"{4+d} 3 1"))+f"\n{1.5+d} 1.5\n-1 -1\n")
    if number == 2767:
        chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ ,.'!?";return "".join(r.choice(chars) for _ in range(r.randint(1,200)))+"\n"
    if number == 2787:
        rows=[" ".join(str(r.randint(1,9)) for _ in range(4)) for _ in range(r.randint(1,12))]
        return "\n".join(rows)+"\n0 0 0 0\n"
    if number == 2927:
        chars=letters+"0123456789 &^$#@*";return "\n".join("".join(r.choice(chars) for _ in range(r.randint(1,80))) for _ in range(r.randint(1,8)))+"\n"
    if number == 2979:
        cases=[]
        for _ in range(r.randint(1,3)):
            n=r.randint(1,20);m=r.randint(1,n);cases.append(f"{n} {m}\n"+"\n".join(f"{r.randint(0,20)} {r.randint(0,20)}" for _ in range(n)))
        return "\n".join(cases)+"\n0 0\n"
    if number == 1008:
        months="pop no zip zotz tzec xul yoxkin mol chen yax zac ceh mac kankin muan pax koyab cumhu uayet".split();rows=[]
        for _ in range(r.randint(1,12)):
            m=r.randrange(19);day=r.randrange(5 if m==18 else 20);rows.append(f"{day}. {months[m]} {r.randint(0,5000)}")
        return f"{len(rows)}\n"+"\n".join(rows)+"\n"
    if number == 1019:
        a=[r.randint(1,2_147_483_647) for _ in range(r.randint(1,10))];return f"{len(a)}\n"+"\n".join(map(str,a))+"\n"
    if number in (1026,2818):
        n=r.randint(1,30);perm=list(range(1,n+1));r.shuffle(perm);rows=[]
        for _ in range(r.randint(1,8)):
            msg="".join(r.choice(letters+" ") for _ in range(r.randint(1,n)));rows.append(f"{r.randint(1,10**6)} {msg}")
        return f"{n}\n"+" ".join(map(str,perm))+"\n"+"\n".join(rows)+"\n0\n0\n"
    if number == 1047:
        return "\n".join("".join(r.choice("0123456789") for _ in range(r.randint(2,35))) for _ in range(r.randint(1,8)))+"\n"
    if number == 1056:
        groups=[]
        for _ in range(r.randint(1,5)):
            codes=set()
            while len(codes)<r.randint(2,8):codes.add("".join(r.choice("01") for _ in range(r.randint(1,10))))
            groups.extend(sorted(codes));groups.append("9")
        return "\n".join(groups)+"\n"
    if number == 1742:
        cases=[]
        for _ in range(r.randint(1,4)):
            n=r.randint(1,20);m=r.randint(1,1000);a=[r.randint(1,100) for _ in range(n)];c=[r.randint(1,20) for _ in range(n)]
            cases.append(f"{n} {m}\n"+" ".join(map(str,a+c)))
        return "\n".join(cases)+"\n0 0\n"
    if number == 1789:
        cases=[]
        for _ in range(r.randint(1,3)):
            codes=set()
            while len(codes)<r.randint(2,30):codes.add("".join(r.choice(letters) for _ in range(7)))
            cases.append(f"{len(codes)}\n"+"\n".join(sorted(codes)))
        return "\n".join(cases)+"\n0\n"
    if number == 1941:return "\n".join(map(str,[r.randint(1,8) for _ in range(r.randint(1,5))]))+"\n0\n"
    if number == 2092:
        cases=[]
        for _ in range(r.randint(1,4)):
            n,m=r.randint(2,20),r.randint(1,20);cases.append(f"{n} {m}\n"+"\n".join(" ".join(str(r.randint(1,60)) for _ in range(m)) for _ in range(n)))
        return "\n".join(cases)+"\n0 0\n"
    if number == 2253:
        cases=[]
        for _ in range(r.randint(1,4)):
            n=r.randint(2,30);cases.append(f"{n}\n"+"\n".join(f"{r.randint(0,1000)} {r.randint(0,1000)}" for _ in range(n)))
        return "\n".join(cases)+"\n0\n"
    if number == 2337:
        # 原写法单词可能重复（违反 n distinct），且随机词几乎全是 ***；改为按欧拉路/回路构造，混入各类无解
        kinds=["path","circuit","path","circuit","degree","disconnected","random"]
        cases=[_cat_case(r,kinds[(seed+k)%len(kinds)],r.randint(3,40),r.randint(2,8)) for k in range(r.randint(1,5))]
        return f"{len(cases)}\n"+"\n".join(cases)+"\n"
    if number == 2676:
        a=[r.randint(1,20) for _ in range(r.randint(1,100))];return f"{len(a)}\n"+" ".join(map(str,a))+"\n"
    if number == 2712:
        md=[31,28,31,30,31,30,31,31,30,31,30,31];days=[]
        for m,d in enumerate(md,1):days.extend((m,x) for x in range(1,d+1))
        rows=[]
        for _ in range(r.randint(1,8)):
            a=r.randint(0,350);b=r.randint(a+1,min(364,a+30));rows.append(f"{days[a][0]} {days[a][1]} {r.randint(1,1000)} {days[b][0]} {days[b][1]}")
        return f"{len(rows)}\n"+"\n".join(rows)+"\n"
    if number == 2883:return "\n".join(" ".join(str(r.randint(-99,99)) for _ in range(5)) for _ in range(r.randint(1,12)))+"\n"
    if number == 2911:return f"{r.randint(1000,9999)}\n"
    if number == 2913:
        chars="".join(chr(i) for i in range(32,123));return "".join(r.choice(chars) for _ in range(r.randint(1,100)))+"\n"
    if number == 1753:return "\n".join("".join(r.choice("bw") for _ in range(4)) for _ in range(4))+"\n"
    raise KeyError(number)


def _cat_words(r, pairs, used, maxlen=20):
    # 按 (首字母, 尾字母) 生成互不相同的单词；单字母词只能用于首尾相同的边
    out = []
    for a, b in pairs:
        while True:
            if a == b and r.random() < 0.15:
                w = a
            else:
                L = r.randint(2, maxlen)
                mid = ''.join(r.choice('abcdefghijklmnopqrstuvwxyz'[:r.choice((3, 26))]) for _ in range(L - 2))
                w = a + mid + b
            if w not in used:
                used.add(w); out.append(w); break
    return out

def _cat_walk(r, n, letters):
    # 在给定字母集上随机游走 n 步，得到一条欧拉路的边序列
    cur = r.choice(letters); pairs = []
    for _ in range(n):
        nxt = r.choice(letters); pairs.append((cur, nxt)); cur = nxt
    return pairs

def _cat_case(r, kind, n, k, maxlen=20):
    letters = r.sample('abcdefghijklmnopqrstuvwxyz', k)
    used = set()
    if kind == "path":
        pairs = _cat_walk(r, n, letters)
    elif kind == "circuit":
        pairs = _cat_walk(r, n - 1, letters); pairs.append((pairs[-1][1], pairs[0][0]))
    elif kind == "degree":
        # 欧拉路上把一条边的尾字母改掉，度数条件被破坏（多数情况下）
        pairs = _cat_walk(r, n, letters); j = r.randrange(n); a, b = pairs[j]
        pairs[j] = (a, r.choice([c for c in 'abcdefghijklmnopqrstuvwxyz' if c != b]))
    elif kind == "disconnected":
        # 两个互不相交字母集上的回路：度数全平衡但不连通
        k1 = max(1, k // 2); A, B = letters[:k1], letters[k1:] or [c for c in 'abcdefghijklmnopqrstuvwxyz' if c not in letters][:1]
        n1 = max(1, n // 2)
        p1 = _cat_walk(r, n1 - 1, A) if n1 > 1 else []
        p1.append((p1[-1][1] if p1 else A[0], p1[0][0] if p1 else A[0]))
        n2 = n - n1
        p2 = _cat_walk(r, n2 - 1, B) if n2 > 1 else []
        p2.append((p2[-1][1] if p2 else B[0], p2[0][0] if p2 else B[0]))
        pairs = p1 + p2
    else:
        pairs = [(r.choice(letters), r.choice(letters)) for _ in range(n)]
    words = _cat_words(r, pairs, used, maxlen)
    r.shuffle(words)
    return f"{len(words)}\n" + "\n".join(words)

def _extra():
    # 追加的覆盖组：最小 n=3、前缀相同的单词（字典序比较含 '.'）、贪心走死胡同、n=1000 满规模各分支
    r = random.Random(23370)
    def fmt(cs):
        return f"{len(cs)}\n" + "\n".join(f"{len(c)}\n" + "\n".join(c) for c in cs) + "\n"
    out = []
    out.append(fmt([["a", "ab", "ba"], ["ab", "b", "ba"], ["aa", "a", "ab"], ["abc", "cba", "xyz"],
                    ["aa", "bb", "ab", "ba"], ["a", "aa", "aaa"]]))
    # 最小字典序的边是桥，Fleury/朴素贪心不回溯会出错
    out.append(fmt([["ab", "ba", "ac", "ca", "ad"], ["ab", "bc", "ca", "ax", "xa", "ay"], ["ab", "abb", "ba", "bab", "bb"],
                    ["cat", "tac", "cot", "toc", "ct"],
                    ["ab", "ac", "ca"], ["ab", "ac", "cd", "da", "bz"], ["aab", "aac", "ca", "bb", "b"]]))
    for kind in ("path", "circuit", "degree", "disconnected", "random"):
        out.append("1\n" + _cat_case(r, kind, 1000, 26) + "\n")
    out.append("1\n" + _cat_case(r, "path", 1000, 3) + "\n")
    out.append("1\n" + _cat_case(r, "circuit", 1000, 2, 20) + "\n")
    out.append(f"20\n" + "\n".join(_cat_case(r, ("path", "circuit", "degree", "disconnected")[i % 4], r.randint(3, 8), r.randint(1, 4), 3) for i in range(20)) + "\n")
    out.append(f"10\n" + "\n".join(_cat_case(r, ("path", "circuit")[i % 2], 1000, r.randint(2, 26)) for i in range(10)) + "\n")
    return out

def valid(text):
    # 首行 t；每组首行 n（3<=n<=1000），随后 n 行各一个 1..20 个小写字母的单词，组内互不相同
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    def isnum(x):
        return x.isdigit() and str(int(x)) == x
    if not lines or not isnum(lines[0]):
        return False
    t = int(lines[0]); i = 1
    if t < 1:
        return False
    for _ in range(t):
        if i >= len(lines) or not isnum(lines[i]):
            return False
        n = int(lines[i]); i += 1
        if not (3 <= n <= 1000) or i + n > len(lines):
            return False
        ws = lines[i:i+n]
        if any(not (1 <= len(w) <= 20 and w.isascii() and w.isalpha() and w.islower()) for w in ws):
            return False
        if len(set(ws)) != n:
            return False
        i += n
    return i == len(lines)

REFERENCE='# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 2337: Catenyms\n# Fenced code block index: 3\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/02337/\n# License: not declared; no license is inferred.\nimport sys\nimport sys\n\n# 增加递归深度以处理 N=1000 的情况\nsys.setrecursionlimit(10000)\n\ndef solve():\n    # 使用 fast I/O 读取所有输入\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n\n    it = iter(input_data)\n    try:\n        t_cases = int(next(it))\n    except StopIteration:\n        return\n\n    for _ in range(t_cases):\n        try:\n            n = int(next(it))\n        except StopIteration:\n            break\n\n        words = []\n        for _ in range(n):\n            words.append(next(it))\n\n        # 1. 字典序排序\n        # 我们希望在 DFS 中先走字典序小的边。\n        # 配合 pop()，我们将单词按降序排列，这样 pop() 拿到的就是最小的单词。\n        words.sort(reverse=True)\n\n        adj = [[] for _ in range(26)]\n        in_deg = [0] * 26\n        out_deg = [0] * 26\n        chars_present = [False] * 26\n\n        for w in words:\n            u = ord(w[0]) - ord(\'a\')\n            v = ord(w[-1]) - ord(\'a\')\n            adj[u].append(w)\n            out_deg[u] += 1\n            in_deg[v] += 1\n            chars_present[u] = chars_present[v] = True\n\n        # 2. 查找起点并检查度数条件\n        start_node = -1\n        out_minus_in_1 = 0\n        in_minus_out_1 = 0\n        possible = True\n\n        for i in range(26):\n            diff = out_deg[i] - in_deg[i]\n            if diff == 1:\n                out_minus_in_1 += 1\n                start_node = i\n            elif diff == -1:\n                in_minus_out_1 += 1\n            elif diff == 0:\n                continue\n            else:\n                possible = False\n                break\n\n        # 欧拉通路判别\n        if not ((out_minus_in_1 == 0 and in_minus_out_1 == 0) or\n                (out_minus_in_1 == 1 and in_minus_out_1 == 1)):\n            possible = False\n\n        if not possible:\n            print("***")\n            continue\n\n        # 如果是欧拉回路，从最小的具有出度的字符开始\n        if start_node == -1:\n            for i in range(26):\n                if out_deg[i] > 0:\n                    start_node = i\n                    break\n\n        # 3. Hierholzer 算法寻找路径\n        res_path = []\n\n        def dfs(u):\n            curr_adj = adj[u]\n            while curr_adj:\n                # 弹出当前节点最小的单词（因为之前是 reverse 排序）\n                w = curr_adj.pop()\n                v = ord(w[-1]) - ord(\'a\')\n                dfs(v)\n                # 后序加入路径\n                res_path.append(w)\n\n        if start_node != -1:\n            dfs(start_node)\n\n        # 4. 连通性检查及输出\n        if len(res_path) != n:\n            print("***")\n        else:\n            # 路径是后序添加的，需要反转\n            print(".".join(reversed(res_path)))\n\nif __name__ == "__main__":\n    solve()\n'
NUMBER=2337
SAMPLE='2\n6\naloha\narachnid\ndog\ngopher\nrat\ntiger\n3\noak\nmaple\nelm\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'s.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout.rstrip()+'\n'
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[generate(NUMBER,s) for s in range(1, 40)]+_extra()):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()
