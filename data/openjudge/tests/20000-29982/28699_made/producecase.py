# 28699 买水果 数据生成器（pctbook M28699 与 practice 28699 共用，两份题面相同）。
# 题面约束：1<=n,m<=100；价格为不超过 100 的正整数；水果名是长度 1..32 的小写拉丁字母串；
# 清单中不同水果数 <= n。
# 第 0 组为题面样例 1，第 1 组为题面样例 2；答案由同目录 samplecode.py 计算。
import random
import string
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = '5 3\n4 2 1 10 5\napple\norange\nmango\n'
SAMPLE2 = '6 5\n3 5 1 6 8 1\npeach\ngrapefruit\nbanana\norange\norange\n'
LOWER = string.ascii_lowercase
FRUITS = ['apple', 'orange', 'mango', 'peach', 'grapefruit', 'banana', 'pear', 'kiwi', 'lemon', 'lime',
          'cherry', 'plum', 'grape', 'melon', 'watermelon', 'papaya', 'apricot', 'fig', 'date', 'guava']


def valid(text):
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    try:
        p = lines[0].split(' ')
        if len(p) != 2 or not all(x.isdigit() and x == str(int(x)) for x in p):
            return False
        n, m = map(int, p)
        if not (1 <= n <= 100 and 1 <= m <= 100) or len(lines) != m + 2:
            return False
        pr = lines[1].split(' ')
        if len(pr) != n or any(not x.isdigit() or x != str(int(x)) or not 1 <= int(x) <= 100 for x in pr):
            return False
        names = lines[2:]
        if any(not 1 <= len(s) <= 32 or any(c not in LOWER for c in s) for s in names):
            return False
        return len(set(names)) <= n
    except ValueError:
        return False


def rand_name(r, lo=1, hi=32):
    return ''.join(r.choice(LOWER) for _ in range(r.randint(lo, hi)))


def distinct_names(r, k, style):
    res, used = [], set()
    while len(res) < k:
        if style == 0 and len(used) < len(FRUITS):
            s = r.choice(FRUITS)
        elif style == 1:
            s = rand_name(r, 1, 3)
        else:
            s = rand_name(r, 1, 32)
        if s not in used:
            used.add(s)
            res.append(s)
    return res


def fmt(prices, items):
    return f"{len(prices)} {len(items)}\n{' '.join(map(str, prices))}\n" + "\n".join(items) + "\n"


def gen(r, s):
    n = r.choice([r.randint(1, 10), r.randint(1, 100), 100])
    m = r.choice([r.randint(1, 10), r.randint(1, 100), 100])
    k = r.randint(1, min(n, m))
    names = distinct_names(r, k, s % 3)
    items = names[:]  # 保证每个名字都出现
    # 出现次数偏斜：部分水果多次出现
    w = [r.choice([1, 1, 2, 5, 20]) for _ in range(k)]
    items += r.choices(names, weights=w, k=m - k)
    r.shuffle(items)
    pmax = r.choice([3, 10, 100])
    prices = [r.randint(1, pmax) for _ in range(n)]
    return fmt(prices, items)


def cases():
    r = random.Random(28699)
    out = [SAMPLE, SAMPLE2]
    out.append(fmt([1], ['a']))                                                  # n=m=1
    out.append(fmt([100] * 100, ['z' * 32] * 100))                               # 一种水果买 100 个
    out.append(fmt([r.randint(1, 100) for _ in range(100)], distinct_names(r, 100, 2)))   # 100 种各一个
    out.append(fmt(list(range(1, 101)), ['kiwi']))                               # n=100,m=1
    out.append(fmt([r.randint(1, 100) for _ in range(100)], ['a', 'aa', 'aaa', 'aaaa'] * 25))   # 前缀相同的名字
    out.append(fmt([7] * 50, distinct_names(r, 10, 0) * 10))                      # 价格全相同
    out.append(fmt([1, 100], ['apple'] * 99 + ['banana']))                        # 次数悬殊
    out.append(fmt([5, 1, 100, 50], ['b', 'a']))                                  # m<n
    out.append(fmt(list(range(100, 0, -1)), [n for i, n in enumerate(distinct_names(r, 13, 1)) for _ in range(i + 1)][:100]))
    for s in range(30):
        out.append(gen(r, s))
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
