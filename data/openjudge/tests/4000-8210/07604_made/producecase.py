import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='n = int(input())\nstring = input()\ndict_ = {} # 注意用dict()或者{}都可以但是不能用dict\nfor i in range(len(string) - n + 1): # 注意要- n + 1\n    if string[i: i + n] in dict_:\n        dict_[string[i: i + n]] += 1\n    else:\n        dict_[string[i: i + n]] = 1\nmaxim_count = max(dict_.values()) # 注意value写法\nif maxim_count <= 1: # 注意是小于等于不是小于\n    print("NO")\nelse:\n    print(maxim_count)\n    for gram in dict_:\n        if dict_[gram] == maxim_count:\n            print(gram)'
SAMPLE='3\nabcdefabcd\n'
GENERATOR_NAME='g7604'
def g7604(r):
    n=r.randint(1,8); s="".join(r.choice("abcde") for _ in range(r.randint(n,40)))
    return f"{n}\n{s}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()
