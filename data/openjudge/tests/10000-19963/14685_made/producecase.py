import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="k, n = map(int, input().split())\nmoney = []\nfor _ in range(n):\n    money.append(int(input()))\n\n# 使用集合加快查找速度\nmoney_set = set(money)\n# 使用集合去重\nfound = set()\nresult = []\n\nfor a in money:\n    b = k - a\n    if b in money_set:\n        # 确保不是同一个元素（当a=b时，需要有两个相同的数）\n        if a != b or money.count(a) > 1:\n            # 标准化组合：较小的在前\n            pair = (min(a, b), max(a, b))\n            if pair not in found:\n                found.add(pair)\n                result.append(pair)\n\n# 排序输出\nresult.sort(key=lambda x: x[0])\nif result:\n    for a, b in result:\n        print(f'{a} {b}')\nelse:\n    print('No Solution')"
SAMPLE='8 9\n-1\n6\n5\n3\n4\n2\n9\n0\n8\n'
GENERATOR_NAME='g14685'
def g14685(r):
    n=r.randint(2,30); k=r.randint(-50,50); z=[r.randint(-50,50) for _ in range(n)]
    return f"{k} {n}\n"+"\n".join(map(str,z))+"\n"

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
