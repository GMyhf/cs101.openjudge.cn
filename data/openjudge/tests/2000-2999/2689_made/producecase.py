import random, subprocess, sys, tempfile
from pathlib import Path
def g2689(r):
    seed = g2689.seed = getattr(g2689, "seed", 0) + 1
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    tricky = "@[\\]^_`{|}~"          # 夹在 A-Z、a-z 前后的非字母，卡 'A'<=c<='z' 之类的错判
    printable = "".join(chr(c) for c in range(32, 127))
    if seed <= 6:
        n = 79                        # 长度上限（小于 80）
    elif seed <= 9:
        n = seed - 6                  # 长度 1..3
    else:
        n = r.randint(1, 79)
    if seed % 4 == 0:
        pool = tricky + letters
    elif seed % 4 == 1:
        pool = printable
    elif seed % 4 == 2:
        pool = letters + " .,;:!?'-"
    else:
        pool = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789"
    if seed == 10: pool = "ABCXYZ"
    if seed == 11: pool = "abcxyz"
    if seed == 12: pool = "0123456789 +-*/=()"   # 没有字母，原样输出
    t = [r.choice(pool) for _ in range(n)]
    t[0] = r.choice(letters + tricky) if seed != 12 else "7"
    t[-1] = r.choice(letters + tricky + ".") if seed != 12 else "9"
    return "".join(t) + "\n"

def valid(text):
    """题面：输入一行待互换的字符串，长度小于 80（按可见 ASCII 与空格核格式）。"""
    if not text.endswith("\n") or text.count("\n")!=1:return False
    t=text[:-1]
    return 1<=len(t)<80 and all(32<=ord(c)<=126 for c in t)

REFERENCE="# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 2689: 大小写字母互换\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/02689/\n# License: not declared in source collection; no license is inferred.\ns = input()\ngap = ord('a') - ord('A')\n\nans = []\nfor i in s:\n    if 'A' <= i <= 'Z':\n        ans += chr(ord(i) + gap)\n    elif 'a' <= i <= 'z':\n        ans += chr(ord(i) - gap)\n    else:\n        ans += i\n\nprint(''.join(ans))\n"
SAMPLE='If so, you already have a Google Account. You can sign in on the right.\n'
GENERATOR='g2689'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1, 40)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
