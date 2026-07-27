import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/20163/\n# Accepted submission: 32204981\n# Source: http://cs101.openjudge.cn/practice/solution/32204981/\n# License: not declared on the submission page; no license is inferred.\n\nn = int(input())\ns = []\nfor i in range(n):\n    s += input().split()\noutput = []\nfor j in range(len(s)):\n    if s[j][0].isupper():\n        # check if it is the start of a sentence\n        if j == 0 or s[j-1] == ".":\n            word = s[j]\n            continue\n        else:\n            if word:\n                word += " " + s[j]\n            else:\n                word = s[j]\n            \n    else:\n        if word and (j != 0 and s[j-2] != ".") and word not in output:\n            output.append(word)\n        word = ""\nif output:\n    print("\\n".join(output))\nelse:\n    print("Khong!")\n'
SAMPLE='2\nNhững mẫu bánh sinh nhật và dễ thương với đủ hình dáng , màu sắc khác nhau khiến ai ngắm nhìn cũng vô cùng thích thú và muốn ngay lập tức lựa chọn chiếc bánh cho bữa tiệc sinh nhật của mình .\nNhững mẫu bánh sinh nhật hình con chó , hình con khỉ .\n'
GENERATOR_NAME='g20163'
def g20163(r):
    words = ["Lan", "Minh", "Hoa", "Mai", "Nam"]
    rows = []
    for _ in range(r.randint(1, 4)):
        rows.append(" ".join(r.choice(words) for _ in range(r.randint(3, 9))) + " .")
    return f"{len(rows)}\n" + "\n".join(rows) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
