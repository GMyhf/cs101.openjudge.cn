import random, subprocess, sys, tempfile
from pathlib import Path
# 固定边界值：最小 1、首个与 7 相关的 6/7/8、含 7 的十位段 70~79、7 的倍数 77/98、最大 99
FIXED_2701 = [1, 2, 6, 7, 8, 13, 14, 17, 20, 27, 49, 69, 70, 71, 76, 77, 78, 79, 80, 97, 98, 99]
def g2701(r, seed):
    if seed <= len(FIXED_2701): return f"{FIXED_2701[seed - 1]}\n"
    rest = [x for x in range(1, 100) if x not in FIXED_2701 and x != 21]
    random.Random(2701).shuffle(rest)
    return f"{rest[seed - len(FIXED_2701) - 1]}\n"

def valid(text):
    """题面：一行，正整数 n（n < 100）。"""
    import re
    m = re.fullmatch(r"([1-9]\d*)\n", text)
    return bool(m) and 1 <= int(m.group(1)) < 100

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
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed), seed) for seed in range(1, 40)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()
