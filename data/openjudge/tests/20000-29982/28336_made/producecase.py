# 28336 / E28336 消消乐 测试数据生成器
# 用法：在本目录下 python3 producecase.py；答案由同目录 samplecode.py 生成。
import random
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = 'abbaca\n'
SAMPLE2 = 'abccddccba\n'
LOWER = 'abcdefghijklmnopqrstuvwxyz'
MAXLEN = 9999  # 长度小于 10^4


def valid(text):
    """严格照题面核输入：一行，只含小写字母，长度 1..9999（小于 10^4）。"""
    return re.fullmatch(r'[a-z]{1,9999}\n', text) is not None


def nested(r, half):
    """嵌套回文 x1 x2 ... xk xk ... x1，相邻不同，整体消光。"""
    s = []
    for _ in range(half):
        s.append(r.choice([c for c in LOWER if not s or c != s[-1]]))
    return ''.join(s) + ''.join(reversed(s))


def no_adjacent(r, n, alpha=LOWER):
    s = []
    for _ in range(n):
        s.append(r.choice([c for c in alpha if not s or c != s[-1]]))
    return ''.join(s)


def rand_reducible(r, n):
    """随机插入成对字母，消得只剩少量。"""
    s = []
    while len(s) < n - 1:
        c = r.choice(LOWER)
        k = r.randint(0, len(s))
        s[k:k] = [c, c]
    return ''.join(s)[:n]


def cases():
    r = random.Random(28336)
    out = [SAMPLE, SAMPLE2]
    out += ['a\n', 'aa\n', 'aaa\n', 'ab\n', 'abba\n']
    # 满长度：全相同（奇数剩一个，偶数消光）
    out.append('a' * MAXLEN + '\n')
    out.append('z' * (MAXLEN - 1) + '\n')
    # 满长度：嵌套回文整体消光（逐轮扫描相邻对的写法要很多轮）
    out.append(nested(r, (MAXLEN - 1) // 2) + '\n')
    # 满长度：没有可消的对，原样输出
    out.append(no_adjacent(r, MAXLEN) + '\n')
    out.append(('ab' * 5000)[:MAXLEN] + '\n')
    # 满长度：两字母随机，大量连锁消除
    out.append(''.join(r.choice('ab') for _ in range(MAXLEN)) + '\n')
    # 满长度：成对插入，几乎消光
    out.append(rand_reducible(r, MAXLEN) + '\n')
    out.append(rand_reducible(r, MAXLEN - 1) + '\n')
    # 满长度：嵌套回文后面接不可消的尾巴
    out.append(nested(r, 4000) + no_adjacent(r, MAXLEN - 8000) + '\n')
    # 满长度：26 字母随机
    out.append(''.join(r.choice(LOWER) for _ in range(MAXLEN)) + '\n')
    # 奇数个连续相同字母（消到只剩一个，与相邻字母再连锁）
    out.append(''.join(c * r.choice([1, 2, 3, 4, 5]) for c in no_adjacent(r, 3000, 'abc'))[:MAXLEN] + '\n')
    # 其余随机组，长度各异
    while len(out) < 30:
        n = r.choice([r.randint(1, 20), r.randint(20, 1000), r.randint(1000, MAXLEN)])
        kind = r.randrange(3)
        if kind == 0:
            s = ''.join(r.choice(LOWER[:r.randint(2, 26)]) for _ in range(n))
        elif kind == 1:
            s = rand_reducible(r, n) if n > 1 else 'q'
        else:
            s = nested(r, n // 2) + no_adjacent(r, n % 2 + r.randint(0, 3))
        out.append(s[:MAXLEN] + '\n')
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
