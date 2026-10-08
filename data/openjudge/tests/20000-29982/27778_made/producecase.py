import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/27778/\n# Accepted submission: 52735575\n# Source: http://cs101.openjudge.cn/practice/solution/52735575/\n# License: not declared on the submission page; no license is inferred.\n\nimport hashlib\n\ndef get_md5(s):\n    # 创建md5对象\n    md5 = hashlib.md5()\n    # 必须编码为 bytes 才能加密\n    md5.update(s.encode(\'utf-8\'))\n    # 返回32位小写十六进制字符串\n    return md5.hexdigest()\n\nT = int(input())\nfor _ in range(T):\n    # 读取两行文本\n    text1 = input()\n    text2 = input()\n    # 计算MD5并比较\n    if get_md5(text1) == get_md5(text2):\n        print("Yes")\n    else:\n        print("No")'
SAMPLE='2\nhelloworld\nworldhello\nhelloworld\nhelloworld\n'
EXTRA_CASE=None
GENERATOR_NAME='g27778'
COLL_A = 'TEXTCOLLBYfGiJUETHQ4hAcKSMd5zYpgqf1YRDhkmxHkhPWptrkoyz28wnI9V0aHeAuaKnak'
COLL_B = 'TEXTCOLLBYfGiJUETHQ4hEcKSMd5zYpgqf1YRDhkmxHkhPWptrkoyz28wnI9V0aHeAuaKnak'
PRINTABLE = ''.join(chr(c) for c in range(33, 127))

def valid(text):
    """题面：第一行 T（1<=T<=10），之后 2T 行文本，每行长度不超过 1000 个字符。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if not lines[0].isdigit() or lines[0] != str(int(lines[0])):
        return False
    t = int(lines[0])
    if not 1 <= t <= 10 or len(lines) != 1 + 2 * t:
        return False
    return all(len(x) <= 1000 and '\r' not in x for x in lines[1:])

def _word(r, lo, hi, alpha):
    return ''.join(r.choice(alpha) for _ in range(r.randint(lo, hi)))

def _pair(r, big):
    alpha = r.choice(["abcXYZ012", PRINTABLE, PRINTABLE + "    "])
    hi = 1000 if big else r.choice([5, 80, 300])
    kind = r.random()
    if kind < .18:  # MD5 碰撞：不同串、相同哈希，直接比较字符串会错
        return (COLL_A, COLL_B) if r.random() < .5 else (COLL_B, COLL_A)
    a = _word(r, max(1, hi - 20) if big else 1, hi, alpha).strip() or 'a'
    if kind < .45:
        return a, a
    b = list(a)
    m = r.random()
    if m < .3:  # 只改一个字符
        i = r.randrange(len(b)); b[i] = r.choice([c for c in "aZ9#" if c != b[i]])
    elif m < .5:  # 大小写不同
        b = list(a.swapcase()) if a.swapcase() != a else b + ['x']
    elif m < .7 and len(a) < 1000:
        b.append(r.choice("xY9"))
    elif m < .85 and len(a) > 1:
        b.pop()
    else:
        b = list(a[::-1]) if a[::-1] != a else b + ['q']
    b = ''.join(b)[:1000].strip() or 'a'  # 变异后也不留首尾空白
    if b == a:
        b = a[:-1] + ('b' if a[-1] != 'b' else 'c')
    return (a, b) if r.random() < .5 else (b, a)

def g27778(r):
    seed = r.random()
    big = seed < .25
    t = 10 if big or r.random() < .4 else r.randint(1, 10)
    rows = [str(t)]
    pairs = [_pair(r, big) for _ in range(t)]
    if r.random() < .6:  # 多数组里放进碰撞对
        pairs[r.randrange(t)] = (COLL_A, COLL_B) if r.random() < .5 else (COLL_B, COLL_A)
    for a, b in pairs:
        rows += [a, b]
    return "\n".join(rows) + "\n"

def g27778_fixed(k):
    if k == 0:  # 仅一组，且是题面提示里的碰撞对
        return "1\n" + COLL_A + "\n" + COLL_B + "\n"
    if k == 1:  # 满规模：10 组、每行 1000 字符，夹带碰撞对与只差末字符的串
        r = random.Random(277781)
        rows = ["10"]
        for i in range(10):
            a = ''.join(r.choice(PRINTABLE) for _ in range(1000))
            if i in (3, 7):
                rows += [COLL_B, COLL_A]
            elif i % 2:
                rows += [a, a]
            else:
                rows += [a, a[:-1] + ('x' if a[-1] != 'x' else 'y')]
        return "\n".join(rows) + "\n"
    # 单字符、相同/不同
    return "3\na\na\na\nb\nA\na\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=90)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def scale_case(): return EXTRA_CASE
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[g27778_fixed(k) for k in range(3)]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 37)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
