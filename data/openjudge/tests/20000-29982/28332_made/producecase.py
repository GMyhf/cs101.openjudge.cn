# 28332 收集金币达成成就 测试数据生成器
# 用法：在本目录下 python3 producecase.py；答案由同目录 samplecode.py 生成。
# 题面允许全空格的行，但「跳过空白行」与「输出 0」两种读法会分歧，生成器不出全空格行。
import random
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = 'xyy xxz\nzz z\nswsw sweet ttuu sswwwtt ttt\na bccba\n'
LOWER = 'abcdefghijklmnopqrstuvwxyz'


def valid(text):
    """严格照题面核输入：若干行，每行长度 1..1000，只含小写字母和空格。"""
    if not text.endswith('\n') or '\r' in text:
        return False
    lines = text[:-1].split('\n')
    return len(lines) >= 1 and all(re.fullmatch(r'[a-z ]{1,1000}', s) for s in lines)


def need(c):
    return 26 - (ord(c) - 97)


def fix(s):
    """保证不是全空格行。"""
    return s if s.strip() else s[:-1] + 'z'


def rand_line(r, n, alpha=LOWER, p_space=0.15):
    return fix(''.join(' ' if r.random() < p_space else r.choice(alpha) for _ in range(n)))


def all_achievements(r, extra_spaces=0):
    """恰好集齐 26 种成就（351 枚金币），随机打乱，达成顺序与字母顺序不同。"""
    coins = [c for c in LOWER for _ in range(need(c))]
    r.shuffle(coins)
    for _ in range(extra_spaces):
        coins.insert(r.randrange(len(coins) + 1), ' ')
    return ''.join(coins)


def threshold_line(r, c, k):
    """字母 c 恰好 k 枚，夹杂其他字母（都不达标）。"""
    coins = [c] * k
    for o in LOWER:
        if o != c:
            coins += [o] * r.randint(0, need(o) - 1)
    r.shuffle(coins)
    return ''.join(coins)[:1000]


def cases():
    r = random.Random(28332)
    out = [SAMPLE]
    # 单字符行：只有 z 一枚就成就
    out.append('z\n')
    out.append('a\n')
    out.append('\n'.join(LOWER) + '\n')
    # 恰好达标 / 差一枚：每种字母各两行
    rows = []
    for c in LOWER:
        rows.append(threshold_line(r, c, need(c)))
        rows.append(threshold_line(r, c, need(c) - 1) if need(c) > 1 else 'y' * 24)
    out.append('\n'.join(rows) + '\n')
    # 集齐全部 26 种，达成顺序是打乱的；达标后继续收集同种金币
    rows = []
    for i in range(40):
        s = all_achievements(r, extra_spaces=r.randint(0, 300))
        if i % 2:
            s += ''.join(r.choice(LOWER) for _ in range(1000 - len(s)))
        rows.append(s[:1000])
    out.append('\n'.join(rows) + '\n')
    # 按字母逆序达成（Z 先于 A），卡按字母表排序输出
    s = ''.join(c * need(c) for c in reversed(LOWER))
    out.append(s + '\n' + s[::-1] + '\n' + ' ' * 649 + s + '\n')
    # 同一字母远超阈值（只能算一次）
    out.append('a' * 1000 + '\n' + 'z' * 1000 + '\n' + ('ab ' * 333)[:1000] + '\n')
    # 首尾空格、连续空格
    rows = []
    for _ in range(50):
        body = rand_line(r, r.randint(1, 500), p_space=0.3)
        rows.append(fix((' ' * r.randint(0, 200) + body + ' ' * r.randint(0, 200))[:1000]))
    out.append('\n'.join(rows) + '\n')
    # 绝大部分是空格，只零星几枚金币
    rows = [fix(''.join(r.choice(LOWER) if r.random() < 0.02 else ' ' for _ in range(1000))) for _ in range(30)]
    out.append('\n'.join(rows) + '\n')
    # 满长度：1000 行 × 1000 字符（两组，金币分布不同）
    out.append('\n'.join(rand_line(r, 1000, p_space=0.1) for _ in range(1000)) + '\n')
    out.append('\n'.join(rand_line(r, 1000, alpha='uvwxyz', p_space=0.05) for _ in range(1000)) + '\n')
    # 单行满长度
    out.append(rand_line(r, 1000, p_space=0.0) + '\n')
    # 其余随机组：行数、行长、空格比例、字母子集各异
    while len(out) < 30:
        k = r.randint(1, 26)
        alpha = ''.join(r.sample(LOWER, k))
        nrows = r.choice([1, r.randint(2, 20), r.randint(20, 200)])
        rows = [rand_line(r, r.randint(1, r.choice([50, 400, 1000])), alpha=alpha,
                          p_space=r.choice([0, 0.1, 0.5])) for _ in range(nrows)]
        out.append('\n'.join(rows) + '\n')
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
    assert len(set(cs)) == len(cs), '组间重复'
    for i, c in enumerate(cs):
        assert valid(c), f'第 {i} 组不合法'
        (d / f'{i}.in').write_text(c)
        (d / f'{i}.out').write_text(run(c))


if __name__ == '__main__':
    main()
