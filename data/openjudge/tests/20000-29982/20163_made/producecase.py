import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/20163/\n# Accepted submission: 32204981\n# Source: http://cs101.openjudge.cn/practice/solution/32204981/\n# License: not declared on the submission page; no license is inferred.\n\nn = int(input())\ns = []\nfor i in range(n):\n    s += input().split()\noutput = []\nfor j in range(len(s)):\n    if s[j][0].isupper():\n        # check if it is the start of a sentence\n        if j == 0 or s[j-1] == ".":\n            word = s[j]\n            continue\n        else:\n            if word:\n                word += " " + s[j]\n            else:\n                word = s[j]\n            \n    else:\n        if word and (j != 0 and s[j-2] != ".") and word not in output:\n            output.append(word)\n        word = ""\nif output:\n    print("\\n".join(output))\nelse:\n    print("Khong!")\n'
SAMPLE='2\nNhững mẫu bánh sinh nhật và dễ thương với đủ hình dáng , màu sắc khác nhau khiến ai ngắm nhìn cũng vô cùng thích thú và muốn ngay lập tức lựa chọn chiếc bánh cho bữa tiệc sinh nhật của mình .\nNhững mẫu bánh sinh nhật hình con chó , hình con khỉ .\n'
GENERATOR_NAME='g20163'

# 题面：第一行 n（段数），接下来 n 行每行一段文章。标点只有半角 ',' 和 '.'，且前后均以一个空格
# 与其他单词隔开；首字母大写的单词其首字母都是英文字母 A~Z（不含以 Đ 等开头的词）。
SAMPLE2 = ('2\nHồ Chí Minh , tên khai sinh là Nguyễn Sinh Cung , là nhà cách mạng .\n'
           'Tuần Báo TIME của Hoa Kỳ bình chọn Hồ Chí Minh là một trong 100 nhân vật có ảnh hưởng lớn nhất trong thế kỷ XX .\n')


def valid(text):
    import re
    if not text.endswith("\n") or text.endswith("\n\n"):
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*", lines[0]):
        return False
    n = int(lines[0])
    if len(lines) != n + 1:
        return False
    for line in lines[1:]:
        toks = line.split(" ")
        if not line or "" in toks:           # 单个空格分隔，行首行尾无多余空格
            return False
        for t in toks:
            if t in (",", "."):
                continue
            if "," in t or "." in t:          # 标点必须独立成词
                return False
            if not all(ch.isalnum() for ch in t):   # 只有逗号句点两种标点
                return False
            if t[0].isupper() and not "A" <= t[0] <= "Z":
                return False
    return True


LOWER = ("những mẫu bánh sinh nhật và dễ thương với đủ hình dáng màu sắc khác nhau khiến ai ngắm nhìn "
         "cũng vô cùng thích thú muốn ngay lập tức lựa chọn chiếc cho bữa tiệc của mình con chó khỉ tên "
         "khai là nhà cách mạng bình một trong nhân vật có ảnh hưởng lớn nhất thế kỷ về thăm cô share "
         "nên sắp khóc rồi được đi học ở trường đại học người dân yêu quý").split()
UPPER = ("Hồ Chí Minh Nguyễn Sinh Cung Tuần Báo TIME Hoa Kỳ XX Thanh Bác Quảng Bình Hà Nội Sài Gòn "
         "Việt Nam Hóa Lan Mai Huế Trần Hưng Lê Lợi Phạm Văn THU Mekong Phú Quốc Hải Phòng").split()
NUMS = ("100", "2019", "7", "1945")


def _cap_run(r, names):
    if names and r.random() < .6:
        return list(r.choice(names))
    return [r.choice(UPPER) for _ in range(r.choice((1, 1, 1, 2, 2, 3, 4)))]


def _sentence(r, cap_p, names, first):
    toks = []
    # 句首：大多数是首字母大写的词（全文第一个词必须是），偶尔是数字或小写词
    if first or r.random() < .85:
        if cap_p and r.random() < .35:
            toks += _cap_run(r, names)          # 句首就是专有名词词组
        else:
            toks.append(r.choice(UPPER))
    else:
        toks.append(r.choice(NUMS + tuple(LOWER)))
    for _ in range(r.randint(0, 14)):
        x = r.random()
        if x < .12:
            if toks[-1] != ",":
                toks.append(",")
        elif x < .12 + cap_p:
            toks += _cap_run(r, names)
        elif x < .17 + cap_p:
            toks.append(r.choice(NUMS))
        else:
            toks.append(r.choice(LOWER))
    if toks[-1] == ",":
        toks.pop()
    return toks + ["."]


def _article(r, paras, sents, cap_p):
    names = [tuple(r.choice(UPPER) for _ in range(r.randint(1, 3))) for _ in range(r.randint(0, 6))]
    rows = []
    for p in range(paras):
        toks = []
        for q in range(r.randint(1, sents)):
            toks += _sentence(r, cap_p, names, p == 0 and q == 0)
        rows.append(" ".join(toks))
    return f"{len(rows)}\n" + "\n".join(rows) + "\n"


def g20163(r, seed):
    if seed == 1:
        return SAMPLE2
    if seed <= 3:      # 原来的形状：全是大写人名
        words = ["Lan", "Minh", "Hoa", "Mai", "Nam"]
        rows = [" ".join(r.choice(words) for _ in range(r.randint(3, 9))) + " ." for _ in range(r.randint(1, 4))]
        return f"{len(rows)}\n" + "\n".join(rows) + "\n"
    if seed <= 9:      # 只有句首单词大写 → Khong!
        return _article(r, r.randint(1, 6), 4, 0.0)
    if seed == 10:     # 每句只有一个大写单词就结束："Hà ." 不是专有名词
        rows = [" ".join(f"{r.choice(UPPER)} ." for _ in range(r.randint(1, 5))) for _ in range(3)]
        return f"{len(rows)}\n" + "\n".join(rows) + "\n"
    if seed <= 25:     # 小中规模
        return _article(r, r.randint(1, 8), 5, r.choice((.03, .08, .15)))
    if seed <= 34:     # 较大
        return _article(r, r.randint(20, 100), 8, r.choice((.05, .1, .2)))
    return _article(r, r.randint(200, 400), 10, r.choice((.05, .1)))

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[g20163(random.Random(s), s) for s in range(1, 40)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
