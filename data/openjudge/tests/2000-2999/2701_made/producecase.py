import random, subprocess, sys, tempfile
from pathlib import Path
def g2701(r): return str(r.randint(1, 99)) + "\n"

REFERENCE="# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 2701: 与7无关的数\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/02701/\n# License: not declared in source collection; no license is inferred.\nn = int(input())\n\n# 初始化平方和变量\nsquare_sum = 0\n\n# 遍历所有小于等于n的正整数\nfor num in range(1, n + 1):\n    # 检查是否与7相关\n    if num % 7 != 0 and '7' not in str(num):  # 不被7整除且十进制表示中不含数字7\n        square_sum += num ** 2  # 累加平方值\n\nprint(square_sum)\n"
SAMPLE='21\n'
GENERATOR='g2701'

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
