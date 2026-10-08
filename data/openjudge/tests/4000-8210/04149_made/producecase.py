import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = '# 熊江凯\nimport sys\n\nMAX = 1 << 15\n\n\nclass DDL:\n    def __init__(self, className="", ddl=0, costTime=0):\n        self.className = className\n        self.ddl = ddl\n        self.costTime = costTime\n\n\ndef main():\n    input = sys.stdin.read\n    data = input().split()\n    idx = 0\n\n    t = int(data[idx])\n    idx += 1\n    results = []\n\n    while t > 0:\n        t -= 1\n        n = int(data[idx])\n        idx += 1\n\n        ddlList = []\n        sum = [0] * MAX\n        dp = [float(\'inf\')] * MAX\n        ans = [""] * MAX\n\n        for i in range(n):\n            className = data[idx]\n            ddl = int(data[idx + 1])\n            costTime = int(data[idx + 2])\n            idx += 3\n            ddlList.append(DDL(className, ddl, costTime))\n            sum[1 << i] = ddlList[i].costTime\n\n        for i in range(1 << n):\n            for j in range(n):\n                if i & (1 << j):\n                    sum[i] = sum[i ^ (1 << j)] + ddlList[j].costTime\n\n        dp[0] = 0\n\n        for i in range(1 << n):\n            for j in range(n):\n                if i & (1 << j):\n                    prev = i ^ (1 << j)\n                    penalty = max(0, sum[i] - ddlList[j].ddl)\n                    if dp[prev] + penalty < dp[i] or ans[i] == "":\n                        dp[i] = dp[prev] + penalty\n                        ans[i] = ans[prev] + ddlList[j].className + \'\\n\'\n                    elif dp[prev] + penalty == dp[i]:\n                        ans[i] = min(ans[i], ans[prev] + ddlList[j].className + \'\\n\')\n\n        results.append(f"{dp[(1 << n) - 1]}\\n{ans[(1 << n) - 1]}".strip())\n\n    print("\\n".join(results))\n\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE = '2 \n3 \nComputer 3 3 \nEnglish 20 1 \nMath 3 2 \n3\nComputer 3 3 \nEnglish 6 3 \nMath 6 3\n'
GENERATOR_NAME = 'g4149'


def valid(text):
    """题面契约：首行正整数 T；每组首行 N（1<=N<=15），随后 N 行"名称 D C"，
    名称为不含空白、不多于 50 个字符的串，D、C 为整数（C>=1，完成需一天或若干天），
    且各组课程名按字典序排列。"""
    lines = [ln for ln in text.split("\n")]
    while lines and lines[-1].strip() == "":
        lines.pop()
    pos = 0

    def nxt():
        nonlocal pos
        if pos >= len(lines):
            return None
        ln = lines[pos].split(); pos += 1
        return ln
    try:
        first = nxt()
        if first is None or len(first) != 1:
            return False
        t = int(first[0])
        if t < 1:
            return False
        for _ in range(t):
            hdr = nxt()
            if hdr is None or len(hdr) != 1:
                return False
            n = int(hdr[0])
            if not 1 <= n <= 15:
                return False
            names = []
            for _ in range(n):
                row = nxt()
                if row is None or len(row) != 3:
                    return False
                name, d, c = row[0], int(row[1]), int(row[2])
                if len(name) > 50 or c < 1:
                    return False
                names.append(name)
            if names != sorted(names):
                return False
    except ValueError:
        return False
    return pos == len(lines)


_LOWER = "abcdefghijklmnopqrstuvwxyz"
_UPPER = _LOWER.upper()


def _names(r, n, style):
    # 名称统一为“首字母大写 + 小写字母”，ASCII 序与忽略大小写的序一致，避免歧义
    pool = set()
    while len(pool) < n:
        if style == "long":
            s = r.choice(_UPPER) + "".join(r.choice("ab") for _ in range(r.randint(40, 49)))
        elif style == "prefix":   # 互为前缀的名字，卡掉不带分隔符拼接比较的写法
            base = r.choice(["Math", "Ma", "M", "Mat", "Phy", "Ph"])
            s = base + "".join(r.choice("ab") for _ in range(r.randint(0, 3)))
        else:
            s = r.choice(_UPPER) + "".join(r.choice(_LOWER) for _ in range(r.randint(0, 9)))
        pool.add(s)
    return sorted(pool)


def _one(r, n, kind):
    names = _names(r, n, "long" if kind == "long" else ("prefix" if kind == "prefix" else "plain"))
    rows = []
    for nm in names:
        if kind == "loose":        # 截止时间都很宽，答案 0，按字典序输出
            d, c = r.randint(200, 1000), r.randint(1, 10)
        elif kind == "tight":      # 截止时间都很紧，罚分大
            d, c = r.randint(1, 3), r.randint(5, 30)
        elif kind == "tie":        # 大量相同 (D, C)，靠字典序打破平局
            d, c = r.choice([(6, 3), (5, 2), (10, 3)])
        else:
            d, c = r.randint(1, 8 * n), r.randint(1, 10)
        rows.append(f"{nm} {d} {c}")
    return f"{n}\n" + "\n".join(rows) + "\n"


# (T, n 范围, 类型)
PLAN = [
    (1, (1, 1), "rand"), (1, (2, 2), "tie"), (3, (1, 4), "rand"), (5, (3, 6), "tie"),
    (5, (3, 6), "prefix"), (4, (5, 8), "rand"), (4, (5, 8), "tie"), (4, (5, 8), "prefix"),
    (3, (6, 8), "tight"), (3, (6, 8), "loose"), (6, (1, 8), "rand"), (6, (1, 8), "tie"),
    (2, (8, 10), "rand"), (2, (8, 10), "long"), (2, (10, 12), "rand"), (2, (10, 12), "tie"),
    (2, (12, 14), "prefix"), (2, (12, 14), "rand"), (1, (15, 15), "rand"), (1, (15, 15), "tie"),
    (1, (15, 15), "loose"), (1, (15, 15), "tight"), (1, (15, 15), "long"), (1, (15, 15), "prefix"),
    (2, (15, 15), "rand"), (2, (15, 15), "tie"), (3, (14, 15), "rand"), (3, (13, 15), "tie"),
    (4, (15, 15), "rand"), (4, (15, 15), "tie"), (5, (15, 15), "rand"), (5, (15, 15), "long"),
    (6, (15, 15), "rand"), (6, (15, 15), "tie"), (8, (15, 15), "rand"), (8, (15, 15), "tie"),
    (8, (1, 15), "rand"), (8, (1, 15), "prefix"), (8, (15, 15), "tight"),
]


def g4149(r, plan):
    t, (lo, hi), kind = plan
    return f"{t}\n" + "".join(_one(r, r.randint(lo, hi), kind) for _ in range(t))

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[g4149(random.Random(seed), PLAN[seed-1]) for seed in range(1, 40)]
    assert all(valid(c) for c in cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
