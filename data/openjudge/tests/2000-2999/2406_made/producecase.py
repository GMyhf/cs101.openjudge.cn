import random, subprocess, sys, tempfile
from pathlib import Path
def g2406(r):
    rows = []
    for _ in range(r.randint(1, 15)):
        base = "".join(r.choice("abcd") for _ in range(r.randint(1, 18)))
        rows.append(base * r.randint(1, 15))
    return "\n".join(rows) + "\n.\n"

REFERENCE="# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 2406: 字符串乘方\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02406/\n# License: not declared in source collection; no license is inferred.\nwhile True:\n    s = input().strip()\n    if s == '.':\n        break\n    len_s = len(s)\n    max_power = 1\n    for i in range(1, len_s // 2 + 1):\n        if len_s % i == 0:\n            a = s[:i]\n            if a * (len_s // i) == s:\n                max_power = max(max_power, len_s // i)\n    print(max_power)\n"
SAMPLE='abcd\naaaa\nababab\n.\n'
GENERATOR='g2406'

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
