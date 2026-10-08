import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# 精确整数解：四项运动按每分钟消耗卡路里从高到低贪心（快跑12/分≤30分，游泳10/分≤60分，单车6/分≤90分，慢走4/分≤180分）。\n# 原外部 AC 解 51284569 用 n/60 浮点计算，在 n=21、88 时 int() 截断少 1，故改用整数分钟计算。\nn, p = map(int, input().split())\nt = 0\nrem = n\nfor rate, cap in ((12, 30), (10, 60), (6, 90), (4, 180)):\n    u = min(rem, cap)\n    t += u * rate\n    rem -= u\nprint(t * p)\n'
LANGUAGE='Python3'
SAMPLE='120 2\n'
GENERATOR_NAME='g18189'
import re
def valid(text):
    """题面：输入为 n,p，均为整数（一行两个整数）。题面未给取值范围。"""
    if not re.fullmatch(r"-?\d+ -?\d+\n", text): return False
    return True

# 各运动时长分界（30/90/180/360 分钟）两侧、最小规模、远超总时长、较大 p
EXTRA=[f"{n} {p}\n" for n,p in ((1,1),(29,7),(30,5),(31,4),(89,3),(90,11),(91,2),(179,6),(180,13),(181,8),(359,9),(360,17),(361,19),(1000,1000),(100000,999))]

def g18189(r): return f"{r.randint(1,600)} {r.randint(1,20)}\n"

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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]+EXTRA
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()
