import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19949 statistics, Accepted solution 52459098.\n# Source: http://cs101.openjudge.cn/practice/solution/52459098/\n# Statistics: http://cs101.openjudge.cn/practice/19949/statistics/\n# License: not declared on submission page; no license inferred\nn=int(input())\nc=0\n\ndef count(query):\n    t=query.split()\n    cnt=0\n    status=False\n    for piece in t:\n        if "###" in piece:\n            if piece.startswith("###") and piece.endswith("###"):\n                if not status:\n                    cnt+=1\n                    status=True\n        else:\n            status=False\n    return cnt\n\nfor _ in range(n):\n    c+=count(input())\n\nprint(c)\n'
LANGUAGE='Python3'
SAMPLE='1\n###John### has an ###apple### .\n'
GENERATOR_NAME='g19949'
def g19949(r):
    n=r.randint(1,10); rows=[]
    for _ in range(n):
        rows.append(" ".join(r.choice(["###Alice###","plain","###Bob###","word","###X###"]) for _ in range(r.randint(2,10))))
    return f"{n}\n"+"\n".join(rows)+"\n"

def valid(text):
    """题面契约：首行整数 N（句子数）；接下来恰 N 行句子，词与词之间用单个空格分隔；
    实体的每个单词形如 ###word###（前后各一个 ###，中间非空且不含 #），普通单词不含 #。
    题面未给 N 与句长上限。"""
    try:
        if not text.endswith("\n"):
            return False
        lines = text[:-1].split("\n")
        n = int(lines[0])
        if n < 1 or str(n) != lines[0] or len(lines) != n + 1:
            return False
        for line in lines[1:]:
            words = line.split(" ")
            for w in words:
                if not w:
                    return False
                if "#" in w:
                    if not (len(w) > 6 and w.startswith("###") and w.endswith("###") and "#" not in w[3:-3]):
                        return False
        return True
    except ValueError:
        return False


_PLAIN = ("the a an of in at to has lives testified about case July hearing recovery art stolen during "
          "World War II daughter representative Democratic , . 's Mrs. Mr. and was is").split()
_NAMES = "John apple Shelley Berkley Babbitt Las Vegas Dominic J. Baranello Nevada Party Beijing Peking University O'Neil".split()


def _sentence(r, length, p_entity):
    words = []
    while len(words) < length:
        if r.random() < p_entity:
            words += ["###" + r.choice(_NAMES) + "###" for _ in range(r.choice([1, 1, 1, 2, 3, 4]))]
        else:
            words.append(r.choice(_PLAIN))
    return " ".join(words[:length])


def extra_cases():
    r = random.Random(199490)
    def doc(n, lo, hi, p):
        return f"{n}\n" + "".join(_sentence(r, r.randint(lo, hi), p) + "\n" for _ in range(n))
    cases = [
        "1\n###Shelley### ###Berkley### , a Democratic representative of Nevada Mrs. ###Babbitt### 's daughter lives in ###Las### ###Vegas### testified about the case in July at a Congressional hearing into the recovery of art stolen during World War II .\n",  # 题面样例 2
        "1\n###Dominic### ###J.### ###Baranello### , an enduring power in Democratic Party\n",
        "1\n###John###\n",                                   # 只有一个实体词
        "2\nno entity here .\nnothing at all\n",            # 答案 0
        "2\nhello ###A###\n###B### world\n",                # 跨行不合并：2 个
        "3\n###A### ###B### ###C###\n###D###\n###E### ###F###\n",
        "1\n###A### , ###B### . ###C### ###D### x ###E###\n",
        doc(1, 3000, 3000, 0.3),                           # 单句很长
        doc(2000, 1, 40, 0.25),                            # 句子多
        doc(500, 5, 30, 0.9),                              # 实体密集
        doc(500, 5, 30, 0.02),                             # 实体稀疏
    ]
    return cases


def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        d=Path(d); src=d/'main.py'
        src.write_text(REFERENCE); cmd=[sys.executable,str(src)]
        if LANGUAGE=="G++":
            exe=d/"main"; subprocess.run(["g++","-std=c++17","-O2",str(src),"-o",str(exe)],check=True)
            cmd=[str(exe)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    cases+=extra_cases()
    assert len(set(cases))==len(cases), "存在重复测试组"
    for i,text in enumerate(cases):
        assert valid(text), i
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()
