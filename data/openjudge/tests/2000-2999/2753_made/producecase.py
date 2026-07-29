import random, subprocess, sys, tempfile
from pathlib import Path
def g2753(r):
    values = [r.randint(1, 20) for _ in range(r.randint(1, 15))]
    return str(len(values)) + "\n" + "\n".join(map(str, values)) + "\n"

REFERENCE="# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 2753: 菲波那契数列\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/02753/\n# License: not declared in source collection; no license is inferred.\ndef f(n):\n    if n <= 2:\n        return 1\n    else:\n        return f(n-1)+f(n-2)\n\n\nn = int(input())\nans = []\nfor _ in range(n):\n    num = int(input())\n    ans.append(f(num))\n\nprint('\\n'.join(map(str, ans)))\n"
SAMPLE='4\n5\n2\n19\n1\n'
GENERATOR='g2753'

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
