import random
REFERENCE="# External reference: /practice/30023/statistics/\n# Accepted submission: 52824900\n# Source: http://cs101.openjudge.cn/practice/solution/52824900/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\nimport re\n\ndef solve():\n    # 读取所有输入数据\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    m = int(input_data[0])\n    n = int(input_data[1])\n    \n    # 读取原子及其分子量\n    weights = {}\n    idx = 2\n    for _ in range(m):\n        atom = input_data[idx]\n        weight = int(input_data[idx+1])\n        weights[atom] = weight\n        idx += 2\n        \n    # 读取待计算的化学式\n    formulas = []\n    for _ in range(n):\n        formulas.append(input_data[idx])\n        idx += 1\n        \n    # 用于匹配原子（一个大写字母或一个大写加一个小写字母）、数字、左括号和右括号的正则表达式\n    token_pattern = re.compile(r'([A-Z][a-z]?|\\d+|\\(|\\))')\n    \n    for formula in formulas:\n        tokens = token_pattern.findall(formula)\n        stack = []\n        \n        for token in tokens:\n            if token == '(':\n                stack.append('(')\n            elif token == ')':\n                # 弹出并累加，直到遇到 '('\n                temp_sum = 0\n                while stack and stack[-1] != '(':\n                    temp_sum += stack.pop()\n                if stack and stack[-1] == '(':\n                    stack.pop()  # 弹出左括号\n                stack.append(temp_sum)\n            elif token.isdigit():\n                val = int(token)\n                if stack:\n                    stack[-1] *= val\n            else:\n                # 如果是原子，将其分子量入栈\n                stack.append(weights.get(token, 0))\n        \n        # 栈中剩余数值的总和即为该化学式的分子量\n        print(sum(stack))\n\nif __name__ == '__main__':\n    solve()"
SAMPLE='8 4\nH 1\nHe 4\nC 12\nO 16\nF 19\nNa 23\nAl 27\nCu 64\n(H2C)He\nCu(OH)2\nH((CO)2F)99\nNa1(Al)1O4H4\n'
GENERATOR_NAME='g30023'
import re as _re

_ATOM = _re.compile(r'[A-Z][a-z]?')
_NUM = _re.compile(r'[1-9][0-9]*')

def _parse(f, table):
    """按题面文法解析化学式，返回 (分子量, 最大嵌套层数)；不合法抛 ValueError。"""
    i, n = 0, len(f)
    stack = [0]; depth = 0; maxd = 0
    last = None          # 刚结束的原子/基团的量，用来乘数量
    while i < n:
        c = f[i]
        if c == '(':
            stack.append(0); depth += 1; maxd = max(maxd, depth); last = None; i += 1
        elif c == ')':
            if depth == 0: raise ValueError('unbalanced')
            v = stack.pop(); depth -= 1
            if v == 0 and f[i - 1] == '(': raise ValueError('empty group')
            stack[-1] += v; last = v; i += 1
        elif c.isdigit():
            m = _NUM.match(f, i)
            if not m or last is None: raise ValueError('bad count')
            k = int(m.group()); stack[-1] += last * (k - 1); last = None; i = m.end()
        else:
            m = _ATOM.match(f, i)
            if not m or m.group() not in table: raise ValueError('bad atom')
            v = table[m.group()]; stack[-1] += v; last = v; i = m.end()
    if depth != 0 or n == 0: raise ValueError('unbalanced')
    return stack[0], maxd

def valid(text):
    """题面：第一行 m n；m 行「原子 分子量」（原子=一个大写字母加零到一个小写字母）；
    n 行化学式（原子、基团、正整数数量拼接），最大括号嵌套层数低于 200。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if not _re.fullmatch(r'[1-9]\d* [1-9]\d*', lines[0]):
        return False
    m, n = map(int, lines[0].split())
    if len(lines) != 1 + m + n:
        return False
    table = {}
    for line in lines[1:1 + m]:
        if not _re.fullmatch(r'[A-Z][a-z]? [1-9]\d*', line):
            return False
        a, w = line.split()
        if a in table:
            return False
        table[a] = int(w)
    for f in lines[1 + m:]:
        if not _re.fullmatch(r'[A-Za-z0-9()]+', f):
            return False
        try:
            _, d = _parse(f, table)
        except ValueError:
            return False
        if d >= 200:
            return False
    return True

# 真实元素符号与取整原子量；含 C/Cl/Co/Cu/Ca、N/Na/Ni/Ne、H/He/Hg 等前缀易混组合
_ELEMENTS = [("H", 1), ("He", 4), ("Li", 7), ("Be", 9), ("B", 11), ("C", 12), ("N", 14), ("O", 16),
             ("F", 19), ("Ne", 20), ("Na", 23), ("Mg", 24), ("Al", 27), ("Si", 28), ("P", 31), ("S", 32),
             ("Cl", 35), ("Ar", 40), ("K", 39), ("Ca", 40), ("Fe", 56), ("Co", 59), ("Ni", 59), ("Cu", 64),
             ("Zn", 65), ("Br", 80), ("Ag", 108), ("Sn", 119), ("I", 127), ("Ba", 137), ("W", 184),
             ("Pt", 195), ("Au", 197), ("Hg", 201), ("Pb", 207), ("U", 238), ("V", 51), ("Y", 89)]

LIMIT = 10 ** 18   # 题面未给值域；控制答案在 64 位有符号整数内

def _count(r, big=True):
    x = r.random()
    if x < .45: return ''
    if x < .55: return '1'
    if x < .9 or not big: return str(r.randint(2, 9))
    return str(r.randint(10, 999))

def _formula(r, atoms, depth, items):
    out = []
    for _ in range(items):
        if depth > 0 and r.random() < .35:
            out.append('(' + _formula(r, atoms, depth - 1, r.randint(1, 3)) + ')' + _count(r))
        else:
            out.append(r.choice(atoms) + _count(r))
    return ''.join(out)

def _chain(r, atoms, depth, count_prob=.03):
    """嵌套 depth 层的链：每层可能在括号内外加原子，数量大多省略。"""
    s = r.choice(atoms) + _count(r, False)
    for _ in range(depth):
        inner = s
        if r.random() < .3: inner = r.choice(atoms) + inner
        if r.random() < .3: inner = inner + r.choice(atoms) + _count(r, False)
        s = '(' + inner + ')' + (str(r.randint(2, 3)) if r.random() < count_prob else r.choice(['', '', '', '1']))
    return s

def _case(r, table, formulas):
    lines = [f"{a} {w}" for a, w in table]
    return f"{len(table)} {len(formulas)}\n" + "\n".join(lines) + "\n" + "\n".join(formulas) + "\n"

def _ok(r, table, f):
    v, d = _parse(f, dict(table))
    return v <= LIMIT and d < 200

def _gen_list(r, table, n, maker):
    atoms = [a for a, _ in table]; res = []
    while len(res) < n:
        f = maker(r, atoms)
        if _ok(r, table, f): res.append(f)
    return res

def _table(r, k):
    t = r.sample(_ELEMENTS, k)
    if r.random() < .5:      # 偶尔换成非真实分子量，防止背表
        t = [(a, r.randint(1, 500)) for a, _ in t]
    return t

def g30023(r):
    # 旧版生成器：固定 8 种原子、仅一层括号；新数据见 build_cases()
    atoms = [("H", 1), ("He", 4), ("C", 12), ("O", 16), ("F", 19), ("Na", 23), ("Al", 27), ("Cu", 64)]
    formulas = []
    for _ in range(r.randint(1, 30)):
        a, b = r.choice(atoms)[0], r.choice(atoms)[0]
        formulas.append(f"{a}{r.randint(1, 4)}({b}{r.randint(1, 3)}){r.randint(1, 4)}")
    return f"{len(atoms)} {len(formulas)}\n" + "\n".join(f"{a} {w}" for a, w in atoms) + "\n" + "\n".join(formulas) + "\n"

def build_cases():
    r = random.Random(30023)
    cases = [SAMPLE]
    cases.append('1 1\nH 1\nH\n')                                    # 最小规模
    cases.append('1 3\nO 16\nO1\nO999\n(O)\n')
    cases.append('4 6\nC 12\nCl 35\nCo 59\nO 16\nCCl\nClC\nCoCO\nCOCl2\nC(Cl)(Co)(O)\nCo2(CO3)3\n')  # 前缀易混
    cases.append('3 3\nN 14\nNa 23\nNi 59\nNNaNi\nNaN3\nNi(NNa)10N\n')
    cases.append('2 2\nH 1\nO 16\n' + '(' * 199 + 'H2O' + ')' * 199 + '\n' + '(' * 199 + 'H' + ')2' * 50 + ')' * 149 + 'O\n')  # 199 层
    cases.append(_case(r, [("Fe", 56), ("C", 12)], ['Fe' + str(10 ** 15), '(C' + str(10 ** 6) + ')' + str(10 ** 6)]))  # 大数量
    # 小规模随机
    for t in range(8):
        tb = _table(r, r.randint(1, 10))
        cases.append(_case(r, tb, _gen_list(r, tb, r.randint(1, 20), lambda r, a: _formula(r, a, 3, r.randint(1, 5)))))
    # 中等：较深嵌套 + 多式
    for t in range(8):
        tb = _table(r, r.randint(5, 25))
        cases.append(_case(r, tb, _gen_list(r, tb, r.randint(50, 200), lambda r, a: _formula(r, a, r.randint(3, 8), r.randint(2, 12)))))
    # 深链（接近 199 层）
    for t in range(7):
        tb = _table(r, r.randint(3, 38))
        cases.append(_case(r, tb, _gen_list(r, tb, r.randint(5, 60), lambda r, a: _chain(r, a, r.randint(150, 199)))))
    # 大规模：多行、长式、全部元素
    for t in range(6):
        tb = _table(r, 38)
        cases.append(_case(r, tb, _gen_list(r, tb, 1500, lambda r, a: _formula(r, a, r.randint(2, 6), r.randint(10, 40)))))
    for t in range(3):
        tb = _table(r, 38)
        cases.append(_case(r, tb, _gen_list(r, tb, 300, lambda r, a: _formula(r, a, 4, r.randint(300, 600)))))
    tb = _table(r, 38)
    cases.append(_case(r, tb, _gen_list(r, tb, 2500, lambda r, a: _chain(r, a, r.randint(1, 199), .01))))
    assert len(cases) == 40, len(cases)   # catalog.json 登记了 0..39 共 40 组
    return cases

from pathlib import Path
import random, subprocess, sys, tempfile
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=build_cases()
    assert all(valid(c) for c in cases)
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
