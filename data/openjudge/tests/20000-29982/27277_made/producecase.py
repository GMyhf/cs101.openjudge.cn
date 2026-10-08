import random, re, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# 读取输入\ncoins = list(map(int, input().split()))\namount = int(input())\n\n# 边界：金额为0直接返回0\nif amount == 0:\n    print(0)\n    exit()\n\nINF = float('inf')\n# dp[i] = 凑出金额i需要的最小硬币数\ndp = [INF] * (amount + 1)\ndp[0] = 0\n\n# 完全背包\nfor coin in coins:\n    for i in range(coin, amount + 1):\n        if dp[i - coin] != INF:\n            dp[i] = min(dp[i], dp[i - coin] + 1)\n\n# 输出答案\nprint(dp[amount] if dp[amount] != INF else -1)"
SAMPLE='1 2 5\n11\n'
GENERATOR_NAME='g27277'
MAXC = 2**31 - 1


def valid(text):
    """题面：第一行 coins（1<=长度<=12，1<=coins[i]<=2^31-1，空格分隔），第二行 amount（0<=amount<=10^4）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    parts = lines[0].split(" ")
    if not (1 <= len(parts) <= 12) or not all(re.fullmatch(r"[1-9][0-9]*", x) for x in parts):
        return False
    if not all(1 <= int(x) <= MAXC for x in parts):
        return False
    if not re.fullmatch(r"0|[1-9][0-9]*", lines[1]):
        return False
    return 0 <= int(lines[1]) <= 10**4


def _fmt(coins, amount):
    return " ".join(map(str, coins)) + f"\n{amount}\n"


def g27277(r, index):
    if index <= 8:
        # 原有风格：小面额，但不再保证有序
        coins = list(set(r.randint(1, 100) for _ in range(r.randint(2, 5))))
        r.shuffle(coins)
        return _fmt(coins, r.randint(0, 10000))
    if index <= 12:
        # 贪心反例：大面额优先不是最优
        base = r.choice([[1, 3, 4], [1, 5, 6, 9], [1, 7, 10], [2, 7, 9, 13], [1, 15, 25], [3, 7, 11, 13]])
        coins = base[:] ; r.shuffle(coins)
        return _fmt(coins, r.randint(10, 10000))
    if index <= 17:
        # 无解：所有面额都是 g 的倍数，amount 不是
        g = r.choice([2, 3, 5, 7, 10])
        coins = list(set(g * r.randint(1, 500) for _ in range(r.randint(1, 12))))
        r.shuffle(coins)
        amount = r.randint(1, 10000)
        while amount % g == 0:
            amount = r.randint(1, 10000)
        return _fmt(coins, amount)
    if index <= 21:
        # 混入超大面额（远大于 amount，最大到 2^31-1）
        small = list(set(r.randint(1, 3000) for _ in range(r.randint(1, 6))))
        big = list(set(r.randint(10**4 + 1, MAXC) for _ in range(r.randint(1, 5))))
        coins = small + big + ([MAXC] if index % 2 else [])
        coins = list(dict.fromkeys(coins))[:12]
        r.shuffle(coins)
        return _fmt(coins, r.randint(0, 10000))
    if index == 22:
        return _fmt([MAXC], 10000)
    if index == 23:
        return _fmt([10000], 10000)
    if index == 24:
        return _fmt([1], 10000)
    if index == 25:
        return _fmt([r.randint(1, 10000) for _ in range(1)] + [MAXC], 0)
    if index == 26:
        return _fmt([7, 3], 1)
    # 满规模：12 种面额、amount 接近 10^4
    coins = list(set(r.randint(1, r.choice([50, 500, 5000])) for _ in range(40)))[:12]
    while len(coins) < 12:
        c = r.randint(1, 10000)
        if c not in coins:
            coins.append(c)
    r.shuffle(coins)
    amount = 10000 if index % 3 == 0 else r.randint(9000, 10000)
    return _fmt(coins, amount)

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=60)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def scale_case():
    if GENERATOR_NAME == 'g26267': return 'A'*1000000+'\n'+'A'*1000+'\n'
    if GENERATOR_NAME == 'g26273': return ('abcdefghij'*10000)+'\n'
    if GENERATOR_NAME == 'g26835':
        e=[(i-1,i,float(i)) for i in range(1,99)]
        for i in range(99):
            for j in range(i+2,min(99,i+12)): e.append((i,j,float(10000+i*99+j)))
        return '99 %d\n'%len(e)+'\n'.join(f'{a} {b} {w:.3f}' for a,b,w in e)+'\n'
    if GENERATOR_NAME == 'g27311': return '100000\n'+' '.join(str(i%10001) for i in range(100000))+'\n'+' '.join(str((i*7)%10001) for i in range(100000))+'\n'
    return None
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[globals()[GENERATOR_NAME](random.Random(s), s) for s in range(1, 40)]
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
