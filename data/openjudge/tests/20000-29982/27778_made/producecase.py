import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/27778/\n# Accepted submission: 52735575\n# Source: http://cs101.openjudge.cn/practice/solution/52735575/\n# License: not declared on the submission page; no license is inferred.\n\nimport hashlib\n\ndef get_md5(s):\n    # 创建md5对象\n    md5 = hashlib.md5()\n    # 必须编码为 bytes 才能加密\n    md5.update(s.encode(\'utf-8\'))\n    # 返回32位小写十六进制字符串\n    return md5.hexdigest()\n\nT = int(input())\nfor _ in range(T):\n    # 读取两行文本\n    text1 = input()\n    text2 = input()\n    # 计算MD5并比较\n    if get_md5(text1) == get_md5(text2):\n        print("Yes")\n    else:\n        print("No")'
SAMPLE='2\nhelloworld\nworldhello\nhelloworld\nhelloworld\n'
EXTRA_CASE=None
GENERATOR_NAME='g27778'
def g27778(r):
    t = r.randint(1, 10); rows = [str(t)]
    for _ in range(t):
        a = "".join(r.choice("abcXYZ012") for _ in range(r.randint(0, 80)))
        b = a if r.random() < .35 else a + r.choice("xY9")
        rows += [a, b]
    return "\n".join(rows) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=90)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def scale_case(): return EXTRA_CASE
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
