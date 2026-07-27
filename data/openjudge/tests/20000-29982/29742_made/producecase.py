import random
REFERENCE="# External reference: /practice/29742/statistics/\n# Accepted submission: 52733624\n# Source: http://cs101.openjudge.cn/practice/solution/52733624/\n# License: not declared on the submission page; no license is inferred.\n\ndef calc(sentence):\n    # 1. 分割成音节列表\n    s = sentence.replace(' ', '')\n    arr = []\n    for i in range(0, len(s), 2):\n        arr.append(s[i:i+2])\n    \n    # 2. 统计 PO -> PI -> PA 数量\n    po = 0   # PO 总数\n    pip = 0  # PO+PI 对数\n    res = 0  # 最终答案\n    \n    for word in arr:\n        if word == 'PA':\n            res += pip\n        elif word == 'PI':\n            pip += po\n        elif word == 'PO':\n            po += 1\n    return res\n\n# 循环读入直到结束\nwhile True:\n    try:\n        line = input()\n        print(calc(line))\n    except:\n        break"
SAMPLE='POPIPA\nPOPOPIPIPAPA\nPOPIPA PIPOPA POPIPAPAPIPOPA\n'
GENERATOR_NAME='g29742'
def g29742(r):
    return " ".join(r.choice(("PO", "PI", "PA")) for _ in range(r.randint(1, 120))) + "\n"

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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
