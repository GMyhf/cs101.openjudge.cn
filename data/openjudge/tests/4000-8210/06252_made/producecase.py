import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'def is_match(pattern, s):\n    m, n = len(pattern), len(s)\n    dp = [[False] * (n + 1) for _ in range(m + 1)]\n    \n    dp[0][0] = True  # 空模式匹配空串\n    \n    # 处理模式开头的 \'*\'\n    for i in range(1, m + 1):\n        if pattern[i - 1] == \'*\':\n            dp[i][0] = dp[i - 1][0]\n        else:\n            break  # 一旦出现非 \'*\'，后面不可能匹配空串\n    \n    for i in range(1, m + 1):\n        for j in range(1, n + 1):\n            if pattern[i - 1] == \'*\':\n                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]\n            elif pattern[i - 1] == \'?\' or pattern[i - 1] == s[j - 1]:\n                dp[i][j] = dp[i - 1][j - 1]\n    \n    return dp[m][n]\n\n\nif __name__ == "__main__":\n    pattern = input().strip()\n    s = input().strip()\n    \n    if is_match(pattern, s):\n        print("matched")\n    else:\n        print("not matched")'
SAMPLE = '1*456?\n11111114567\n'
GENERATOR_NAME = 'g6252'
def g6252(r):
    p="".join(r.choice("abc*?") for _ in range(r.randint(2,10)))
    s="".join(r.choice("abc") for _ in range(r.randint(0,12)))
    return f"{p}\n{s}\n"

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
