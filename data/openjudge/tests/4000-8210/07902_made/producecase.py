import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='def max_peanuts(M, N, K, field):\n    # 提取所有有花生的位置及其数量\n    peanuts = []\n    for i in range(M):\n        for j in range(N):\n            if field[i][j] > 0:\n                peanuts.append((field[i][j], i, j))\n    \n    # 按照花生数量从大到小排序\n    peanuts.sort(reverse=True, key=lambda x: x[0])\n    \n    # 初始化当前时间和采摘的花生总数\n    current_time = 0\n    total_peanuts = 0\n    \n    # 初始位置设为路边\n    current_pos = (-1, 0)\n    \n    for peanut in peanuts:\n        amount, x, y = peanut\n        \n        # 计算从当前位置到该位置的时间\n        if current_pos[0] == -1:  # 从路边跳到第一行\n            time_to_reach = x + 1 + abs(current_pos[1] - y)\n        else:\n            time_to_reach = abs(current_pos[0] - x) + abs(current_pos[1] - y)\n        \n        if current_pos == (-1, 0):  # 从路边跳到第一行的时间\n            current_time += (x + 1)\n        else:\n            current_time += time_to_reach\n        \n        # 采摘花生需要1单位时间\n        current_time += 1\n        \n        if current_time + x + 1 <= K:\n            total_peanuts += amount\n            current_pos = (x, y)\n        else:\n            break\n    \n    return total_peanuts\n\n# 读取输入\nM, N, K = map(int, input().split())\nfield = []\nfor _ in range(M):\n    field.append(list(map(int, input().split())))\n\n# 计算并输出结果\nresult = max_peanuts(M, N, K, field)\nprint(result)\n'
SAMPLE='6 7 21\n0 0 0 0 0 0 0\n0 0 0 0 13 0 0\n0 0 0 0 0 0 7\n0 15 0 0 0 0 0\n0 0 0 9 0 0 0\n0 0 0 0 0 0 0\n'
GENERATOR_NAME='g7902'
def g7902(r):
    m,n=r.randint(2,8),r.randint(2,8); k=r.randint(10,120)
    z=[[0]*n for _ in range(m)]
    for _ in range(r.randint(1,min(12,m*n))):
        z[r.randrange(m)][r.randrange(n)]=r.randint(1,30)
    return f"{m} {n} {k}\n"+"\n".join(" ".join(map(str,x)) for x in z)+"\n"

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
