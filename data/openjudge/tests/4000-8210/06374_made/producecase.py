import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'n = int(input())\np = input()\n\nline_char_num = 0\nword_list = p.split(" ")\noutput = [[]]\nfor word in word_list:\n    if len(word) + line_char_num > 80:\n        output.append([])\n        output[-1].append(word)\n        line_char_num = len(word)+1\n    else:\n        output[-1].append(word)\n        line_char_num += len(word)+1\n\nfor line in output:\n    print(" ".join(line))\n\n'
SAMPLE = '84\nOne sweltering day, I was scooping ice cream into cones and told my four children they could "buy" a cone from me for a hug. Almost immediately, the kids lined up to make their purchases. The three youngest each gave me a quick hug, grabbed their cones and raced back outside. But when my teenage son at the end of the line finally got his turn to "buy" his ice cream, he gave me two hugs. "Keep the changes," he said with a smile.\n'
GENERATOR_NAME = 'g6374'
def g6374(r):
    z=["".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(r.randint(1,15))) for _ in range(r.randint(6,40))]
    return f"{len(z)}\n{' '.join(z)}\n"

def valid(text):
    """题面：第一行 n(n<=300)；其后 n 个以空格分隔的单词（含紧邻标点），每个单词长度不大于 40。
    数据约定：单词全在第二行，单个空格分隔，单词由可见 ASCII 字符组成。"""
    try:
        lines = text.split("\n")
        if len(lines) != 3 or lines[2] != "": return False
        if lines[0] != str(int(lines[0])): return False
        n = int(lines[0])
        if not (1 <= n <= 300): return False
        words = lines[1].split(" ")
        if len(words) != n: return False
        return all(1 <= len(w) <= 40 and all(33 <= ord(c) <= 126 for c in w) for w in words)
    except Exception:
        return False

LOW = "abcdefghijklmnopqrstuvwxyz"
def word(r, L):
    w = "".join(r.choice(LOW) for _ in range(L))
    if L >= 2 and r.random() < .3:
        w = w[:-1] + r.choice(",.;:!?")
    if L >= 3 and r.random() < .1:
        w = '"' + w[1:-1] + '"'
    if r.random() < .2:
        w = w[0].upper() + w[1:]
    return w

def mk(ws):
    return f"{len(ws)}\n{' '.join(ws)}\n"

def exact80(r, n):
    # 刻意凑出恰好 80 字符的行，以及差一个字符就放得下（81）的情况
    ws = []
    while len(ws) < n:
        rest = 80
        while rest > 0 and len(ws) < n:
            L = min(rest, r.randint(1, 40))
            if r.random() < .5 and rest <= 40: L = rest
            if r.random() < .15 and rest + 1 <= 40: L = rest + 1
            ws.append(word(r, L)); rest -= L + 1
    return mk(ws)

EXTRA = [
    lambda r: mk([word(r, 1)]),
    lambda r: mk(["a" * 40]),
    lambda r: mk(["b" * 40, "c" * 39]),
    lambda r: mk(["d" * 40, "e" * 40]),
    lambda r: mk(["p" * 40, "q" * 39, "r"]),
    lambda r: mk([word(r, 40) for _ in range(300)]),
    lambda r: mk([word(r, 1) for _ in range(300)]),
    lambda r: mk([word(r, r.randint(1, 40)) for _ in range(300)]),
    lambda r: mk([word(r, r.randint(1, 12)) for _ in range(300)]),
    lambda r: exact80(r, 300),
    lambda r: exact80(r, 150),
    lambda r: exact80(r, 40),
]

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    cases+=[f(random.Random(2000+i)) for i,f in enumerate(EXTRA)]
    assert all(valid(c) for c in cases)
    assert len(set(cases))==len(cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
