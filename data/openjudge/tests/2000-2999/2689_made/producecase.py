import random, subprocess, sys, tempfile
from pathlib import Path
def g2689(r):
    return "".join(r.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789") for _ in range(r.randint(1, 79))) + "\n"

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
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1,21)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
