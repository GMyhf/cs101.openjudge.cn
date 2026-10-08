import random,re,subprocess,tempfile
from collections import Counter
from pathlib import Path
REFERENCE_SOURCE='import sys\nfrom collections import Counter\ndef ok(v):\n if len(v)<2 or (len(v)-2)%3: return "XIANGGONG"\n def f(c,p):\n  if not sum(c.values()): return p is not None\n  x=min(k for k,v in c.items() if v)\n  if p is None and c[x]>=2:\n   c[x]-=2\n   if f(c,x): return True\n   c[x]+=2\n  if c[x]>=3:\n   c[x]-=3\n   if f(c,p): return True\n   c[x]+=3\n  if c.get(x+1,0) and c.get(x+2,0):\n   for y in (x,x+1,x+2): c[y]-=1\n   if f(c,p): return True\n   for y in (x,x+1,x+2): c[y]+=1\n  return None\n return "HU" if f(Counter(v),None) else "BUHU"\nout=[]\nfor line in sys.stdin:\n v=list(map(int,line.split()))\n if v and v[0]==0: break\n out.append(ok(v))\nprint("\\n".join(out))'
SAMPLE_IN='1 2\n4 4\n1 1 1 2 3 4 5 6 7 8 9 9 9\n1 1 1 2 3 4 5 6 7 8 9 9 9 9\n0\n'
def valid(text):
    """题面契约：每行一组，由 1-9 的数字组成、空格分隔；每个数字至多 4 个、元素数 <= 14；
    以开头为 0 的一行结束（之后不再有数据）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if lines[-1] != "0":
        return False
    for line in lines[:-1]:
        if not re.fullmatch(r"[1-9]( [1-9])*", line):
            return False
        v = line.split(" ")
        if len(v) > 14 or max(Counter(v).values()) > 4:
            return False
    return True


def rand_hand(r, size):
    """随机手牌，满足每个数字至多 4 个。"""
    pool = [d for d in range(1, 10) for _ in range(4)]
    return r.sample(pool, size)


def hu_hand(r, melds):
    """由 melds 个刻子/顺子加一个对子拼出的必胡手牌（每个数字至多 4 个），打乱顺序。"""
    for _ in range(1000):
        c = Counter()
        x = r.randint(1, 9); c[x] += 2
        for _ in range(melds):
            if r.random() < 0.4:
                y = r.randint(1, 9); c[y] += 3
            else:
                y = r.randint(1, 7)
                for z in (y, y + 1, y + 2): c[z] += 1
        if max(c.values()) <= 4:
            v = list(c.elements()); r.shuffle(v)
            return v
    raise AssertionError("hu_hand")


def near_hu(r, melds):
    """把一手胡牌改掉一张（仍守住每数字至多 4 个），多数变成不胡、少数仍胡，卡贪心写法。"""
    while True:
        v = hu_hand(r, melds)
        k = r.randrange(len(v)); v[k] = r.randint(1, 9)
        if max(Counter(v).values()) <= 4:
            return v


def g3527(r):
    lines = []
    for _ in range(r.randint(3, 12)):
        t = r.random()
        if t < 0.3:
            lines.append(hu_hand(r, r.randint(0, 4)))
        elif t < 0.6:
            lines.append(near_hu(r, r.randint(1, 4)))
        elif t < 0.85:
            lines.append(rand_hand(r, r.choice([2, 5, 8, 11, 14])))
        else:
            lines.append(rand_hand(r, r.randint(1, 14)))
    return "\n".join(" ".join(map(str, v)) for v in lines) + "\n0\n"


FIXED = [
    # 边界：单张、对子/非对子、14 张满、九莲宝灯式、多种拆法都要回溯
    "1\n9 9\n1 9\n1 1 1 1 2 2 2 2 3 3 3 3 4 4\n1 1 1 2 3 4 5 6 7 8 9 9 9 9\n1 1 2 2 3 3 4 4 5 5 6 6 7 7\n"
    "2 2 2 3 3 3 4 4 4 5 5\n1 1 2 2 3 3 4\n9 9 9 9 8 8 8 8 7 7 7 7 6 6\n1 2 3 4 5 6 7 8 9 1 2 3 5 5\n"
    "1 2 3 4 5 6 7 8 9 1 2 3 4 6\n3 3 3 4 5\n3 4 5 5 5\n1 1 1 2 2\n1 2 3 5 7\n0\n",
]


def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE);handle.flush()
        root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
        for index in range(40):
            if index==0:content=SAMPLE_IN
            elif index<=len(FIXED):content=FIXED[index-1]
            else:
                for attempt in range(100):
                    content=g3527(random.Random(3527+index+attempt*1000))
                    if content not in seen:break
                else:raise AssertionError("insufficient diversity")
            assert valid(content), index
            seen.append(content)
            result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
            (root/f"{index}.in").write_text(content,encoding="utf-8")
            (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")


if __name__ == "__main__":
    main()
