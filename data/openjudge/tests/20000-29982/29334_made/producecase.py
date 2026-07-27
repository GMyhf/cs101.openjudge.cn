import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/29334/\n# Accepted submission: 52829500\n# Source: http://cs101.openjudge.cn/practice/solution/52829500/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef titleToNumber(columnTitle: str) -> int:\n    ans = 0\n    for char in columnTitle:\n        # 计算字符对应的数值 (A -> 1, B -> 2, ..., Z -> 26)\n        value = ord(char) - ord(\'A\') + 1\n        ans = ans * 26 + value\n    return ans\n\nif __name__ == "__main__":\n    # 读取标准输入\n    input_data = sys.stdin.read().split()\n    if input_data:\n        columnTitle = input_data[0]\n        print(titleToNumber(columnTitle))'
SAMPLE='A\n'
EXTRA_CASE=None
GENERATOR_NAME='g29334'
def g29334(r):
    value = r.randint(1, 2_147_483_647); s = ""
    while value: value, rem = divmod(value - 1, 26); s = chr(65 + rem) + s
    return s + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+([EXTRA_CASE] if EXTRA_CASE else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
