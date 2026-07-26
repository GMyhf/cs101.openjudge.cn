import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = '# 熊江凯\nimport sys\n\nMAX = 1 << 15\n\n\nclass DDL:\n    def __init__(self, className="", ddl=0, costTime=0):\n        self.className = className\n        self.ddl = ddl\n        self.costTime = costTime\n\n\ndef main():\n    input = sys.stdin.read\n    data = input().split()\n    idx = 0\n\n    t = int(data[idx])\n    idx += 1\n    results = []\n\n    while t > 0:\n        t -= 1\n        n = int(data[idx])\n        idx += 1\n\n        ddlList = []\n        sum = [0] * MAX\n        dp = [float(\'inf\')] * MAX\n        ans = [""] * MAX\n\n        for i in range(n):\n            className = data[idx]\n            ddl = int(data[idx + 1])\n            costTime = int(data[idx + 2])\n            idx += 3\n            ddlList.append(DDL(className, ddl, costTime))\n            sum[1 << i] = ddlList[i].costTime\n\n        for i in range(1 << n):\n            for j in range(n):\n                if i & (1 << j):\n                    sum[i] = sum[i ^ (1 << j)] + ddlList[j].costTime\n\n        dp[0] = 0\n\n        for i in range(1 << n):\n            for j in range(n):\n                if i & (1 << j):\n                    prev = i ^ (1 << j)\n                    penalty = max(0, sum[i] - ddlList[j].ddl)\n                    if dp[prev] + penalty < dp[i] or ans[i] == "":\n                        dp[i] = dp[prev] + penalty\n                        ans[i] = ans[prev] + ddlList[j].className + \'\\n\'\n                    elif dp[prev] + penalty == dp[i]:\n                        ans[i] = min(ans[i], ans[prev] + ddlList[j].className + \'\\n\')\n\n        results.append(f"{dp[(1 << n) - 1]}\\n{ans[(1 << n) - 1]}".strip())\n\n    print("\\n".join(results))\n\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE = '2 \n3 \nComputer 3 3 \nEnglish 20 1 \nMath 3 2 \n3\nComputer 3 3 \nEnglish 6 3 \nMath 6 3\n'
GENERATOR_NAME = 'g4149'
def g4149(r):
    n=r.randint(2,7); z=[(f"C{i}",r.randint(2,30),r.randint(1,8)) for i in range(n)]
    return "1\n"+f"{n}\n"+"\n".join(f"{a} {b} {c}" for a,b,c in z)+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()
