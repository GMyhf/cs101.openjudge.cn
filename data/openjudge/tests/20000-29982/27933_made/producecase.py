import random, subprocess, sys, tempfile
from pathlib import Path

REFERENCE = "# External reference: statistics page /practice/27933/\n# Accepted submission: 52735532\n# Source: http://cs101.openjudge.cn/practice/solution/52735532/\n# License: not declared on the submission page; no license is inferred.\n\nn = int(input())\nstack = []\nres = 0\ntarget = 1\n\nfor _ in range(2 * n):\n    parts = input().split()\n    if parts[0] == 'add':\n        x = int(parts[1])\n        stack.append(x)\n    else:\n        if stack:\n            # 栈顶正好是要弹出的数字 → 正常弹出\n            if stack[-1] == target:\n                stack.pop()\n            else:\n                # 必须重排一次\n                res += 1\n                stack = []  # 重排后栈内元素有序，直接清空\n        target += 1\n\nprint(res)"

SAMPLE = '3\nadd 1\nremove\nadd 2\nadd 3\nremove\nremove\n'
SAMPLE2 = '7\nadd 3\nadd 2\nadd 1\nremove\nadd 4\nremove\nremove\nremove\nadd 6\nadd 7\nadd 5\nremove\nremove\nremove\n'


def _int(s):
    return s.isdigit() and s[0] != '0'


def valid(text):
    """题面：1≤n≤1e4；2n 行命令，恰 n 个 add（编号 1..n 各一次）、n 个 remove；
    第 k 次 remove 要弹 k 号盒子，故此前 k 号盒子必须已经 add。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if not _int(lines[0]):
        return False
    n = int(lines[0])
    if not (1 <= n <= 10 ** 4) or len(lines) != 2 * n + 1:
        return False
    added = set(); removed = 0
    for ln in lines[1:]:
        if ln == 'remove':
            removed += 1
            if removed > n or removed not in added:
                return False
        else:
            p = ln.split(' ')
            if len(p) != 2 or p[0] != 'add' or not _int(p[1]):
                return False
            x = int(p[1])
            if not 1 <= x <= n or x in added:
                return False
            added.add(x)
    return len(added) == n and removed == n


def fmt(n, cmds):
    return f"{n}\n" + "\n".join(cmds) + "\n"


def gen(r, n, p_remove, order):
    """order: 'rand' 随机加入顺序；'near' 倾向先加小号；'rev' 倾向逆序成块加入。
    只在第 k 号盒子已加入时才可能 remove，保证合法。"""
    pending = list(range(1, n + 1))
    if order == 'rand':
        r.shuffle(pending)
    elif order == 'rev':
        blocks = []
        i = 1
        while i <= n:
            b = r.randint(1, 8); blocks.append(list(range(min(n, i + b - 1), i - 1, -1))); i += b
        pending = [x for blk in blocks for x in blk]
    elif order == 'near':
        pending = list(range(1, n + 1))
        for i in range(n - 1):
            j = min(n - 1, i + r.randint(0, 3)); pending[i], pending[j] = pending[j], pending[i]
    pending.reverse()  # 用 pop() 依次取
    added = set(); k = 1; cmds = []
    while k <= n:
        if k in added and (not pending or r.random() < p_remove):
            cmds.append('remove'); k += 1
        else:
            x = pending.pop(); added.add(x); cmds.append(f'add {x}')
    return fmt(n, cmds)


def build_cases():
    r = random.Random(27933)
    N = 10 ** 4
    cases = [SAMPLE, SAMPLE2]
    cases.append(fmt(N, [f'add {i}' for i in range(1, N + 1)] + ['remove'] * N))            # 答案 1
    cases.append(fmt(N, [f'add {i}' for i in range(N, 0, -1)] + ['remove'] * N))            # 答案 0
    cases.append(fmt(N, [c for i in range(1, N + 1) for c in (f'add {i}', 'remove')]))      # 答案 0
    cases.append(fmt(N, [c for i in range(1, N + 1, 2) for c in (f'add {i}', f'add {i + 1}', 'remove', 'remove')]))  # 答案 n/2
    # 先压入一大批，再反复“压一个新盒子再弹”，每次都要重排且栈很大（卡每次重排都整栈排序的写法）
    h = N // 2
    odd = list(range(1, N + 1, 2)); r.shuffle(odd)
    cmds = [f'add {i}' for i in odd]
    for i in range(1, h + 1):
        cmds += [f'add {2 * i}', 'remove', 'remove']
    cases.append(fmt(N, cmds))                                                          # 答案 n/2
    cmds = [f'add {i}' for i in range(N, h, -1)]
    for i in range(1, h + 1, 2):
        cmds += [f'add {i}', f'add {i + 1}', 'remove', 'remove']
    cmds += ['remove'] * (N - h)
    cases.append(fmt(N, cmds))
    cases.append(gen(r, N, 0.5, 'rand'))
    cases.append(gen(r, N, 0.3, 'near'))
    cases.append(gen(r, N, 0.6, 'rev'))
    # 边界
    cases += [fmt(1, ['add 1', 'remove']), fmt(2, ['add 1', 'add 2', 'remove', 'remove']),
              fmt(2, ['add 2', 'add 1', 'remove', 'remove']), fmt(2, ['add 1', 'remove', 'add 2', 'remove']),
              fmt(3, ['add 2', 'add 1', 'remove', 'add 3', 'remove', 'remove']),
              fmt(3, ['add 3', 'add 1', 'remove', 'add 2', 'remove', 'remove']),
              fmt(4, ['add 1', 'add 3', 'remove', 'add 2', 'remove', 'remove', 'add 4', 'remove'])]
    while len(cases) < 41:
        t = len(cases) % 3
        n = r.choice([r.randint(3, 12), r.randint(13, 300), r.randint(301, N)])
        cases.append(gen(r, n, r.choice([0.1, 0.3, 0.5, 0.8, 0.95]), ['rand', 'near', 'rev'][t]))
    return cases


def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p = Path(d) / 'main.py'; p.write_text(REFERENCE)
        x = subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=90)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout


def main():
    d = Path('data'); d.mkdir(exist_ok=True)
    cases = build_cases()
    assert len(cases) == len(set(cases)), '组间有重复'
    for i, c in enumerate(cases):
        assert valid(c), f'第 {i} 组不合题面'
        (d / f'{i}.in').write_text(c); (d / f'{i}.out').write_text(run(c))


if __name__ == '__main__':
    main()
