# 28416 Taki的乐队梦想（数据强化版） 数据生成器。
# 题面（同 28413，强化）：T=20（除样例外每组都是 20），n<=3000；姓名由字母和数字组成；
# 每名队员的相关人员序号严格小于自己（从 1 计）；保证输出总长度不超过 500kB。
# 第 0 组为题面样例（T=3）；答案由同目录 samplecode.py 计算。
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = '3\n3\nA\nB 1\nC 2 1\n4\nA\nB 1\nC 2\nD 3\n5\nTakamatsu\nKaname\nShiina 2\nChihaya 1\nNagasaki 1 4\n'
TMAX, NMAX, OUT_LIMIT = 20, 3000, 500000
ALNUM = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'


def out_len(names, deps):
    # 输出两行：联系次数、以空格分隔的姓名
    cnt = [0] * len(names)
    chars = [0] * len(names)
    for i, ds in enumerate(deps):
        cnt[i] = 1 + sum(cnt[d] for d in ds)
        chars[i] = len(names[i]) + sum(chars[d] for d in ds)
    m = sum(cnt)
    return len(str(m)) + 1 + sum(chars) + (m - 1) + 1


def valid(text):
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    pos = 0
    try:
        t = lines[pos]
        pos += 1
        # 题面写明“现在T=20”；只有第 0 组沿用 28413 的样例（T=3）
        if not t.isdigit() or not (int(t) == TMAX or text == SAMPLE):
            return False
        total = 0
        for _ in range(int(t)):
            s = lines[pos]
            pos += 1
            if not s.isdigit() or not 1 <= int(s) <= NMAX:
                return False
            n = int(s)
            names, deps = [], []
            for i in range(n):
                ln = lines[pos]
                pos += 1
                parts = ln.split(' ')
                if not parts[0] or any(c not in ALNUM for c in parts[0]):
                    return False
                ds = []
                for p in parts[1:]:
                    if not p.isdigit() or p != str(int(p)):
                        return False
                    v = int(p)
                    if not 1 <= v <= i:   # 严格小于自己的序号 i+1
                        return False
                    ds.append(v - 1)
                if len(set(ds)) != len(ds):
                    return False
                names.append(parts[0])
                deps.append(ds)
            total += out_len(names, deps)
        return pos == len(lines) and total <= OUT_LIMIT
    except (IndexError, ValueError):
        return False


def make_names(r, n, style):
    used, res = set(), []
    while len(res) < n:
        if style == 'short':
            k = r.choice([1, 1, 2, 2, 2, 3])
        elif style == 'long':
            k = r.randint(8, 20)
        else:
            k = r.randint(1, 8)
        s = ''.join(r.choice(ALNUM) for _ in range(k))
        if s not in used:
            used.add(s)
            res.append(s)
    return res


def build(r, n, budget, style, maxdeg, shuffle=True, chain=0):
    """按输出预算随机造依赖；chain>0 时前 chain 人连成一条链。"""
    names = make_names(r, n, style)
    deps, cnt, chars = [], [], []
    used = len(str(n)) + 2
    suf = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = suf[i + 1] + len(names[i]) + 1
    for i in range(n):
        rest = suf[i + 1]          # 后面每人至少贡献自己的名字和一个空格
        ds = []
        extra = 0
        if chain and 0 < i < chain:
            ds = [i - 1]
        elif i and maxdeg:
            k = r.randint(0, min(i, maxdeg))
            for d in r.sample(range(i), k):
                add = chars[d] + cnt[d]
                if used + len(names[i]) + 1 + extra + add + rest + 12 <= budget:
                    ds.append(d)
                    extra += add
        c = 1 + sum(cnt[d] for d in ds)
        ch = len(names[i]) + sum(chars[d] for d in ds)
        if used + ch + c + rest + 12 > budget and ds:
            ds, c, ch = [], 1, len(names[i])
        deps.append(ds)
        cnt.append(c)
        chars.append(ch)
        used += ch + c
    rows = [str(n)]
    for i in range(n):
        ds = [d + 1 for d in deps[i]]
        if shuffle:
            r.shuffle(ds)
        else:
            ds.sort()
        rows.append(' '.join([names[i]] + list(map(str, ds))))
    assert out_len(names, deps) <= budget
    return rows


def tiny(r):
    n = r.randint(1, 9)
    return build(r, n, 5000, r.choice(['short', 'mid', 'long']), r.randint(0, 4), r.random() < 0.7)


def case(tests):
    return '\n'.join([str(len(tests))] + [x for rows in tests for x in rows]) + '\n'


def cases():
    r = random.Random(28416)
    per = OUT_LIMIT // TMAX - 100
    out = [SAMPLE]
    # 满规模：20 组 n=3000，输出把预算用满
    out.append(case([build(r, NMAX, per, 'short', 3) for _ in range(TMAX)]))
    out.append(case([build(r, NMAX, per, 'mid', 6) for _ in range(TMAX)]))
    # 一组 n=3000 吃掉几乎全部输出预算（卡 ans=ans+part 之类的逐次复制写法）
    out.append(case([build(r, NMAX, OUT_LIMIT - 2000, 'short', 4)] + [tiny(r) for _ in range(TMAX - 1)]))
    # 长链（深递归）+ 满规模
    out.append(case([build(r, NMAX, 470000, 'short', 0, chain=650)] + [tiny(r) for _ in range(TMAX - 1)]))
    # 全部没有依赖
    out.append(case([build(r, NMAX, per, 'mid', 0) for _ in range(TMAX)]))
    # 依赖度很大
    out.append(case([build(r, NMAX, per, 'short', 40) for _ in range(TMAX)]))
    # 边界（题面规定 T=20，小测试点重复 20 次凑满）：n=1；全是 n=1；纯数字姓名
    out.append(case([['1', 'Taki']] * TMAX))
    out.append(case([['1', ''.join(r.choice(ALNUM) for _ in range(r.randint(1, 6)))] for _ in range(TMAX)]))
    out.append(case([['3', '0', '1 1', '2 1 2']] * TMAX))
    out.append(case([['2', 'a', 'b 1']] * TMAX))
    out.append(case([['4', 'A', 'B', 'C 2 1', 'D 3 2 1']] * TMAX))
    # 小规模随机，依赖序号乱序给出
    for _ in range(12):
        out.append(case([tiny(r) for _ in range(TMAX)]))
    # 中等规模
    for k in range(17):
        tests = []
        for _ in range(TMAX):
            n = r.randint(10, 400)
            tests.append(build(r, n, n * 22 + r.randint(500, 6000), r.choice(['short', 'mid', 'long']), r.choice([1, 2, 3, 8]),
                               r.random() < 0.6))
        out.append(case(tests))
    return out


def run(text):
    x = subprocess.run([sys.executable, str(HERE / 'samplecode.py')], input=text,
                       text=True, capture_output=True, timeout=120)
    if x.returncode:
        raise SystemExit(x.stderr)
    return x.stdout


def main():
    d = HERE / 'data'
    d.mkdir(exist_ok=True)
    cs = cases()
    assert len(cs) == 41 and len(set(cs)) == len(cs), len(cs)
    for i, c in enumerate(cs):
        assert valid(c), i
        (d / f'{i}.in').write_text(c)
        (d / f'{i}.out').write_text(run(c))


if __name__ == '__main__':
    main()
