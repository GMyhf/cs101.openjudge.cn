import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/22549/\n# Accepted submission: 52824884\n# Source: http://cs101.openjudge.cn/practice/solution/52824884/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef main():\n    # 读取所有输入并去除两端的空白字符\n    try:\n        s = sys.stdin.read().strip()\n    except Exception:\n        print(-1)\n        return\n\n    # 如果输入为空，则不存在不重复的字符，输出 -1\n    if not s:\n        print(-1)\n        return\n\n    # 统计每个字符出现的次数\n    char_count = {}\n    for char in s:\n        char_count[char] = char_count.get(char, 0) + 1\n\n    # 寻找第一个出现次数为 1 的字符\n    for index, char in enumerate(s):\n        if char_count[char] == 1:\n            print(index)\n            return\n            \n    # 若无符合条件的字符，输出 -1\n    print(-1)\n\nif __name__ == '__main__':\n    main()"
SAMPLE='perpendicular\n'
GENERATOR_NAME='g22549'
def g22549(r):
    letters="abcdefghijklmnopqrstuvwxyz"; n=r.randint(1,60)
    return "".join(r.choice(letters) for _ in range(n))+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
