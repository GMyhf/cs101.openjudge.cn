import random, subprocess, sys, tempfile
from pathlib import Path
# 参考解：槽位计数法。原来内嵌的 AC 提交（45199466）在「一棵完整树之后又接了一棵以相同数字开头的树」
# （如 1 # # 1 # #）时会误判为 T，这里换成按题意的严格写法：遍历中途槽位耗尽或最终槽位不为 0 都是 F。
REFERENCE = '''import sys
def check(ls):
    slots = 1
    for t in ls:
        if slots == 0:
            return False
        slots += 1 if t != '#' else -1
    return slots == 0

data = sys.stdin.read().split()
p = 0
out = []
while True:
    n = int(data[p]); p += 1
    if n == 0:
        break
    ls = data[p:p + n]; p += n
    out.append('T' if check(ls) else 'F')
print('\\n'.join(out))
'''
SAMPLE = '13\n9 3 4 # # 1 # # 2 # 6 # #\n4\n9 # # 1\n2\n# 99\n0\n'
MAXN = 200000


def valid(text):
    """题面：多组数据，每组两行：正整数 N（1<=N<=200000）；N 个空格分隔的元素，
    每个是 # 或小于 100 的正整数。最后一行为 0。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if lines[-1] != '0' or len(lines) % 2 != 1 or len(lines) < 3:
        return False
    for i in range(0, len(lines) - 1, 2):
        s = lines[i]
        if not s.isdigit() or s != str(int(s)):
            return False
        n = int(s)
        if not 1 <= n <= MAXN:
            return False
        toks = lines[i + 1].split(' ')
        if len(toks) != n:
            return False
        for t in toks:
            if t == '#':
                continue
            if not t.isdigit() or t != str(int(t)) or not 1 <= int(t) <= 99:
                return False
    return True


def val(r):
    return str(r.randint(1, 99))


def rand_tree(r, k, bias=None):
    """k 个非空节点的随机前序序列（含 k+1 个 #），迭代生成，不受递归深度限制。
    bias 控制放数字的倾向：越大树越深。"""
    out = []; slots = 1; left = k
    while slots:
        if left and (slots == 1 or r.random() < (bias if bias is not None else left / (left + slots))):
            out.append(val(r)); left -= 1; slots += 1
        else:
            if slots == 1 and left:
                out.append(val(r)); left -= 1; slots += 1
                continue
            out.append('#'); slots -= 1
    assert left == 0 and len(out) == 2 * k + 1
    return out


def left_chain(r, k):
    return [val(r) for _ in range(k)] + ['#'] * (k + 1)


def right_chain(r, k):
    out = []
    for _ in range(k):
        out += [val(r), '#']
    return out + ['#']


def zigzag(r, k):
    """左右交替的长链：偶数号节点的孩子在左（右为 #），奇数号节点的孩子在右（左为 #）。"""
    out = []; tail = []
    for i in range(k - 1):
        out.append(val(r))
        if i % 2 == 0:
            tail.append('#')        # 右孩子空，等左子树写完再补
        else:
            out.append('#')         # 左孩子空
    out += [val(r), '#', '#']
    return out + tail[::-1]


def is_ok(ls):
    slots = 1
    for t in ls:
        if slots == 0:
            return False
        slots += 1 if t != '#' else -1
    return slots == 0


def mutate_bad(r, ls):
    """把合法序列改成非法序列，覆盖多种出错方式。"""
    kind = r.randrange(6)
    if kind == 0 and len(ls) > 1:            # 截断
        cut = r.randint(1, len(ls) - 1)
        res = ls[:-cut]
    elif kind == 1:                           # 完整树后再接一棵以相同数字开头的树（森林）
        res = ls + [ls[0]] + ['#', '#']
    elif kind == 2:                           # 完整树后多一个 #
        res = ls + ['#']
    elif kind == 3:                           # 完整树后多一个数字
        res = ls + [val(r)]
    elif kind == 4 and len(ls) >= 3:          # 把最后一个 # 挪到前面某处，中途槽位可能提前耗尽
        res = ls[:-1]
        j = r.randint(1, len(res))
        res = res[:j] + ['#'] + res[j:]
    else:                                     # 数字与 # 互换一处，数量关系被破坏
        i = r.randrange(len(ls))
        res = ls[:]
        res[i] = '#' if res[i] != '#' else val(r)
    if res and is_ok(res):
        res = res + ['#']
    return res if res else ['#', '#']


def small_tests(r, cnt, maxk):
    tests = []
    for _ in range(cnt):
        k = r.randint(1, maxk)
        ls = rand_tree(r, k)
        if r.random() < .5:
            ls = mutate_bad(r, ls)
        if len(ls) > MAXN:
            ls = ls[:MAXN]
        tests.append(ls)
    return tests


def fmt(tests):
    return ''.join(f"{len(t)}\n{' '.join(t)}\n" for t in tests) + '0\n'


def big_case(r, kind):
    k = (MAXN - 1) // 2      # 99999 个节点 -> N = 199999
    if kind == 'rand':
        return [rand_tree(r, k)]
    if kind == 'deep':
        return [rand_tree(r, k, bias=.75)]
    if kind == 'left':
        return [left_chain(r, k)]
    if kind == 'right':
        return [right_chain(r, k)]
    if kind == 'zig':
        return [zigzag(r, k)]
    if kind == 'forest':      # 199997 的合法树 + 同首数字的 3 元素树 = 200000
        t = rand_tree(r, k - 1)
        return [t + [t[0], '#', '#']]
    if kind == 'trunc':
        return [rand_tree(r, k)[:-1]]
    if kind == 'early':       # 前缀就是一棵完整的小树，后面还有大量元素
        t = rand_tree(r, 3)
        return [t + rand_tree(r, k - 4)[:-1]]
    if kind == 'extra':
        return [rand_tree(r, k - 1) + ['#']]
    if kind == 'swap':
        t = rand_tree(r, k)
        i = r.randrange(len(t) // 2, len(t))
        while t[i] != '#':
            i -= 1
        t[i] = val(r)
        return [t]
    raise ValueError(kind)


def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p = Path(d) / 'main.py'; p.write_text(REFERENCE)
        x = subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=60)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout


def main():
    d = Path('data'); d.mkdir(exist_ok=True)
    cases = [SAMPLE]
    # 1：极小与刁钻的手工组（N=1 的数字、N=3 合法、森林 1 # # 1 # #、首元素为 # 等）
    cases.append(fmt([['5'], ['1', '#', '#'], ['1', '#', '#', '1', '#', '#'], ['#', '1', '#'],
                      ['7', '#'], ['7', '#', '#', '#'], ['1', '2', '#', '#', '#'], ['1', '#', '2', '#', '#'],
                      ['3', '3', '#', '#', '3', '#', '#'], ['3', '#', '#', '3', '#', '#', '#'],
                      ['99', '#', '#'], ['1', '1', '1']]))
    # 2..13：每个文件多组小规模
    for s in range(2, 14):
        r = random.Random(22460 * 100 + s)
        cases.append(fmt(small_tests(r, r.randint(5, 30), r.choice([3, 8, 20, 60]))))
    # 14..21：中等规模多组
    for s in range(14, 22):
        r = random.Random(22460 * 100 + s)
        cases.append(fmt(small_tests(r, r.randint(3, 10), r.choice([500, 2000, 5000]))))
    # 22..39：满规模（N 接近 200000），T/F 各种结构
    kinds = ['rand', 'deep', 'left', 'right', 'zig', 'forest', 'trunc', 'early', 'extra', 'swap',
             'rand', 'deep', 'left', 'forest', 'swap', 'trunc', 'right', 'zig']
    for s, kind in zip(range(22, 40), kinds):
        r = random.Random(22460 * 100 + s)
        tests = big_case(r, kind)
        if s % 2:
            tests = small_tests(r, 3, 5) + tests
        cases.append(fmt(tests))
    assert len(cases) == 40 and len(set(cases)) == 40
    for i, c in enumerate(cases):
        assert valid(c), i
        assert len(c.encode()) <= 1 << 20, i
        (d / f'{i}.in').write_text(c); (d / f'{i}.out').write_text(run(c))


if __name__ == '__main__': main()
