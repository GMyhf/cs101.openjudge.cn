import random, subprocess, tempfile
from pathlib import Path
# 原 REFERENCE_SOURCE（多题合一的 P=4035 分支）有错：方块拖进空列后，原列上方的方块不下落，
# 导致漏解/错解。这里换成独立重写、带正确下落的 DFS（剪枝：不做向左交换、不交换同色、某色不足 3 块即失败）。
REFERENCE_SOURCE="import sys\ndef parse(s):\n    a=s.split();n=int(a[0]);p=1;cols=[]\n    for x in range(5):\n        c=[]\n        while int(a[p]):c.append(int(a[p]));p+=1\n        p+=1;cols.append(tuple(c))\n    return n,tuple(cols)\ndef settle(cols):\n    cols=[list(c) for c in cols]\n    while True:\n        rm=set()\n        for x in range(5):\n            c=cols[x]\n            for y in range(len(c)-2):\n                if c[y]==c[y+1]==c[y+2]:rm|={(x,y),(x,y+1),(x,y+2)}\n        for y in range(7):\n            for x in range(3):\n                if all(len(cols[x+t])>y for t in range(3)) and cols[x][y]==cols[x+1][y]==cols[x+2][y]:\n                    rm|={(x,y),(x+1,y),(x+2,y)}\n        if not rm:return tuple(tuple(c) for c in cols)\n        cols=[[v for y,v in enumerate(cols[x]) if (x,y) not in rm] for x in range(5)]\ndef domove(cols,x,y,d):\n    q=x+d\n    if not 0<=q<5 or y>=len(cols[x]):return None\n    c=[list(t) for t in cols]\n    if y<len(c[q]):\n        c[x][y],c[q][y]=c[q][y],c[x][y]\n    else:\n        if len(c[q])>=7:return None\n        v=c[x].pop(y);c[q].append(v)\n    return settle(c)\ndef solve(n,cols,prune=True):\n    fail=set();path=[]\n    def dfs(b,left):\n        if left==0:return all(len(c)==0 for c in b)\n        if (b,left) in fail:return False\n        if prune:\n            cnt={}\n            for c in b:\n                for v in c:cnt[v]=cnt.get(v,0)+1\n            if any(v<3 for v in cnt.values()):fail.add((b,left));return False\n        for x in range(5):\n            for y in range(len(b[x])):\n                for d in (1,-1):\n                    if prune:\n                        q=x+d\n                        if 0<=q<5 and y<len(b[q]) and (d==-1 or b[q][y]==b[x][y]):continue\n                    z=domove(b,x,y,d)\n                    if z is None:continue\n                    path.append((x,y,d))\n                    if dfs(z,left-1):return True\n                    path.pop()\n        fail.add((b,left));return False\n    return list(path) if dfs(cols,n) else None\ndef fmt(r):\n    return '-1\\n' if r is None else ''.join(f'{x} {y} {d}\\n' for x,y,d in r)\nif __name__=='__main__':\n    n,cols=parse(sys.stdin.read())\n    print(fmt(solve(n,cols,prune='--noprune' not in sys.argv)),end='')\n"
SAMPLE_IN='3 \n1 0 \n2 1 0 \n2 3 4 0 \n3 1 0 \n2 4 3 4 0\n'

_ns = {"__name__": "mayan_ref"}
exec(REFERENCE_SOURCE, _ns)


def _parse_board(text):
    """把 text 解析成 (n, cols)；格式不对返回 None。行尾空白放过（题面样例带行尾空格）。"""
    if not text.endswith("\n"):
        return None
    lines = [ln.rstrip(" ") for ln in text[:-1].split("\n")]
    if len(lines) != 6:
        return None
    try:
        rows = []
        for ln in lines:
            if ln == "" or ln.startswith(" ") or "  " in ln:
                return None
            rows.append([int(x) for x in ln.split(" ")])
    except ValueError:
        return None
    if len(rows[0]) != 1:
        return None
    cols = []
    for row in rows[1:]:
        if row[-1] != 0 or any(v == 0 for v in row[:-1]) or len(row) - 1 > 7:
            return None
        cols.append(tuple(row[:-1]))
    return rows[0][0], tuple(cols)


def valid(text):
    """题面契约：第一行 0<n<=5；5 行各描述一列（自下而上的颜色，以 0 结束，每列至多 7 块）；
    颜色 1..10 且从 1 开始顺序编号；初始棋盘没有可消除的方块。"""
    parsed = _parse_board(text)
    if parsed is None:
        return False
    n, cols = parsed
    if not 1 <= n <= 5:
        return False
    used = {v for c in cols for v in c}
    if not used or any(not 1 <= v <= 10 for v in used) or used != set(range(1, max(used) + 1)):
        return False
    return _ns["settle"](cols) == cols


def candidate(r, C, nb, bottom=False, short=0):
    cnt = [3] * C
    for _ in range(max(0, nb - 3 * C)):
        cnt[r.randrange(C)] += 1
    for _ in range(short):                    # 让某种颜色不足 3 块
        cnt[r.randrange(C)] = r.randint(1, 2)
    vals = [c + 1 for c in range(C) for _ in range(cnt[c])]
    r.shuffle(vals)
    cols = [[] for _ in range(5)]
    for v in vals:
        free = [x for x in range(5) if (not cols[x] if bottom else len(cols[x]) < 7)]
        if not free:
            return None
        cols[r.choice(free)].append(v)
    return tuple(tuple(c) for c in cols)


def text_of(n, cols):
    return f"{n}\n" + "\n".join(" ".join(map(str, list(c) + [0])) for c in cols) + "\n"


# (n, 是否有解, 形态)；形态：plain / bottom（只在最下一行）/ short（某色不足 3 块）/ tall（有一列堆满 7 块）
SLOTS = (
    [(1, True, "bottom"), (2, True, "bottom"), (3, True, "bottom"), (2, False, "bottom"), (3, False, "bottom")]
    + [(1, True, "plain")] * 3 + [(2, True, "plain")] * 3 + [(3, True, "plain")] * 4
    + [(4, True, "plain")] * 4 + [(5, True, "plain")] * 6
    + [(5, False, "plain")] * 6 + [(1, False, "plain"), (2, False, "plain"), (3, False, "plain"), (4, False, "plain")]
    + [(5, False, "short"), (3, False, "short"), (5, False, "tall"), (5, True, "tall")]
)


def pick(i, n, want, shape, seen=()):
    r = random.Random(4035 * 1000 + i)
    solve = _ns["solve"]
    for _attempt in range(200000):
        C = r.randint(1, 4) if shape != "tall" else r.randint(2, 4)
        if shape == "bottom":
            # 只在最下一行：至多 5 块。单色 3~5 块，或两色且一色不足 3 块
            if r.random() < 0.5:
                cols = candidate(r, 1, r.randint(3, 5), bottom=True)
            else:
                cols = candidate(r, 2, 3, bottom=True, short=1)
        elif shape == "tall":
            cols = candidate(r, C, r.randint(9, 15))
            if cols is not None and max(map(len, cols)) < 7:
                continue
        else:
            cols = candidate(r, C, r.randint(3 * C, min(3 * C + 4, 15)), short=1 if shape == "short" else 0)
        if cols is None or _ns["settle"](cols) != cols:
            continue
        got = solve(n, cols)
        if (got is not None) != want:
            continue
        if want and n >= 2 and solve(n - 1, cols) is not None and r.random() < 0.7:
            continue                          # 尽量让 n 恰为最少步数
        # 题面没说能否做“同色交换”这种空操作；只收两种理解下答案一致的局面
        if _ns["solve"](n, cols, prune=False) != got:
            continue
        text = text_of(n, cols)
        if text not in seen and valid(text):
            return text
    raise AssertionError(f"slot {i} 找不到合适局面")


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py") as h:
        h.write(REFERENCE_SOURCE)
        h.flush()
        root = Path(__file__).parent / "data"
        seen = set()
        for i in range(40):
            c = SAMPLE_IN if i == 0 else pick(i, *SLOTS[i - 1], seen=seen)
            assert valid(c) and c not in seen, i
            seen.add(c)
            p = subprocess.run(["python3", h.name], input=c, text=True, capture_output=True, check=True)
            (root / f"{i}.in").write_text(c)
            (root / f"{i}.out").write_text(p.stdout)


if __name__ == "__main__":
    main()
