import random
REFERENCE="# External reference: /practice/29742/statistics/\n# Accepted submission: 52733624\n# Source: http://cs101.openjudge.cn/practice/solution/52733624/\n# License: not declared on the submission page; no license is inferred.\n\ndef calc(sentence):\n    # 1. 分割成音节列表\n    s = sentence.replace(' ', '')\n    arr = []\n    for i in range(0, len(s), 2):\n        arr.append(s[i:i+2])\n    \n    # 2. 统计 PO -> PI -> PA 数量\n    po = 0   # PO 总数\n    pip = 0  # PO+PI 对数\n    res = 0  # 最终答案\n    \n    for word in arr:\n        if word == 'PA':\n            res += pip\n        elif word == 'PI':\n            pip += po\n        elif word == 'PO':\n            po += 1\n    return res\n\n# 循环读入直到结束\nwhile True:\n    try:\n        line = input()\n        print(calc(line))\n    except:\n        break"
SAMPLE='POPIPA\nPOPOPIPIPAPA\nPOPIPA PIPOPA POPIPAPAPIPOPA\n'
GENERATOR_NAME='g29742'

def valid(text):
    """题面契约：若干行（至少一行），每行由 PO/PI/PA 组成，空格只出现在音节之间
    （不在行首行尾、不在音节内部）。题面未给行数与长度上限，只核格式。"""
    import re
    if not text.endswith('\n') or text == '\n':
        return False
    line = re.compile(r'(PO|PI|PA)( *(PO|PI|PA))*')
    return all(line.fullmatch(l) for l in text[:-1].split('\n'))

def _line(r, n, mode, weights=(1, 1, 1)):
    syl = r.choices(("PO", "PI", "PA"), weights=weights, k=n)
    if mode == 'none':
        return "".join(syl)
    if mode == 'one':
        return " ".join(syl)
    out = [syl[0]]
    for s in syl[1:]:
        out.append(" " * r.choice((0, 0, 1, 1, 2, 3)) + s)
    return "".join(out)

def g29742(r, idx):
    modes = ('none', 'one', 'mix')
    if idx == 1:
        lines = ["PO", "PI", "PA", "PAPIPO", "PO PI PA", "POPIPA"]
    elif idx == 2:
        lines = ["PA PI PO PA PI PO", "PAPAPAPIPIPIPOPOPO", "PIPAPO", "POPAPI"]   # 全 0 与逆序
    elif idx <= 20:
        lines = [_line(r, r.randint(1, 40), r.choice(modes)) for _ in range(r.randint(2, 15))]
    elif idx <= 28:
        lines = [_line(r, r.randint(100, 3000), r.choice(modes)) for _ in range(r.randint(5, 30))]
    elif idx <= 34:
        # 长句：答案远超 2^31，卡 O(n^2)/O(n^3) 与 32 位整型
        lines = [_line(r, r.randint(60000, 100000), r.choice(modes)) for _ in range(r.randint(1, 3))]
    elif idx == 35:
        n = 100000; lines = ["PO" * n + "PI" * n + "PA" * n]
    elif idx == 36:
        n = 30000; lines = [" ".join(["PO"] * n + ["PI"] * n + ["PA"] * n)]
    elif idx == 37:
        lines = [_line(r, 100000, 'mix', (5, 1, 1)), _line(r, 100000, 'none', (1, 1, 5))]
    elif idx == 38:
        lines = [_line(r, r.randint(1, 5), r.choice(modes)) for _ in range(5000)]   # 行很多
    else:
        lines = ["PA" * 50000 + "PI" * 50000 + "PO" * 50000]
    return "\n".join(lines) + "\n"

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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed), seed) for seed in range(1, 40)]
    for i, case in enumerate(cases):
        assert valid(case), i
        assert len(case) <= 1 << 20, i
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
