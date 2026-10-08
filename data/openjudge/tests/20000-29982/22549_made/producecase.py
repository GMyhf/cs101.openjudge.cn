import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/22549/\n# Accepted submission: 52824884\n# Source: http://cs101.openjudge.cn/practice/solution/52824884/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef main():\n    # 读取所有输入并去除两端的空白字符\n    try:\n        s = sys.stdin.read().strip()\n    except Exception:\n        print(-1)\n        return\n\n    # 如果输入为空，则不存在不重复的字符，输出 -1\n    if not s:\n        print(-1)\n        return\n\n    # 统计每个字符出现的次数\n    char_count = {}\n    for char in s:\n        char_count[char] = char_count.get(char, 0) + 1\n\n    # 寻找第一个出现次数为 1 的字符\n    for index, char in enumerate(s):\n        if char_count[char] == 1:\n            print(index)\n            return\n            \n    # 若无符合条件的字符，输出 -1\n    print(-1)\n\nif __name__ == '__main__':\n    main()"
SAMPLE='perpendicular\n'
GENERATOR_NAME='g22549'
def g22549(r):
    letters="abcdefghijklmnopqrstuvwxyz"; n=r.randint(1,60)
    return "".join(r.choice(letters) for _ in range(n))+"\n"

def valid(text):
    # 题面：一个字符串，长度在 100,000 以内，只由小写英文字母组成（单行）
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    line = text[:-1]
    return 1 <= len(line) <= 100000 and all("a" <= ch <= "z" for ch in line)

def special_cases():
    r = random.Random(22549)
    N = 100000
    L = "abcdefghijklmnopqrstuvwxyz"
    out = []
    out.append("z\n")                                    # 长度 1，答案 0
    out.append("abcabc\n")                               # 提示，答案 -1
    out.append("aa\n")                                   # 最小的 -1
    s = [r.choice(L) for _ in range(N // 2)] * 2
    r.shuffle(s); out.append("".join(s) + "\n")          # 满规模，每个字母出现偶数次 -> -1
    t = [r.choice(L[:25]) for _ in range(N - 1)]
    out.append("".join(t) + "z\n")                       # 满规模，唯一字符在最后
    u = list(L[:25] * (N // 25))[:N - 1]; r.shuffle(u)
    u.insert(N // 2, "z"); out.append("".join(u) + "\n") # 满规模，唯一字符在中间
    return out

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 34)]+special_cases()
    for c in cases: assert valid(c), c[:80]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
