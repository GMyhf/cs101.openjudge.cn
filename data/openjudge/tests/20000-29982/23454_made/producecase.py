import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/23454/\n# Accepted submission: 52297305\n# Source: http://cs101.openjudge.cn/practice/solution/52297305/\n# License: not declared on the submission page; no license is inferred.\n\ns=input()\nans=''\nfound=False\nfor i in range(len(s)):\n    if s[i]!=' ':\n        ans+=s[i]\n        if found==True:\n            found=False\n    elif found==False:\n        ans+=s[i]\n        found=True\nprint(ans)"
SAMPLE='Boy        next    door\n'
GENERATOR_NAME='g23454'
def valid(text):
    # 题面：一行，一个字符串（不包含标点符号），句子的头和尾都没有空格
    # （格式核对：只允许 ASCII 字母、数字和空格，非空）
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    line = text[:-1]
    if not line or line[0] == " " or line[-1] == " ":
        return False
    return all(ch == " " or (ch.isascii() and ch.isalnum()) for ch in line)

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def _word(r):
    w = "".join(r.choice(LETTERS) for _ in range(r.randint(1, 10)))
    if r.random() < 0.1:
        w = str(r.randint(0, 2024))
    return w

def g23454(r):
    words = [_word(r) for _ in range(r.randint(2, 12))]
    out = words[0]
    for w in words[1:]:
        out += " " * (1 if r.random() < 0.3 else r.randint(2, 10)) + w
    return out + "\n"

def special_cases():
    r = random.Random(23454)
    out = ["Hello\n", "a\n", "I am a student of Peking University\n", "a" + " " * 1000 + "b\n"]
    words = [_word(r) for _ in range(9000)]
    big = words[0]
    for w in words[1:]:
        big += " " * r.choice([1, 1, 2, 3, 5, 8, 13]) + w
    out.append(big + "\n")                                   # 长句，混合间隔
    out.append(" ".join(["x"] * 20000).replace("x x", "x" + " " * 3 + "x") + "\n")  # 长句，单字符单词
    return out

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 34)]+special_cases()
    assert len(set(cases)) == len(cases)
    for c in cases: assert valid(c), c[:80]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
