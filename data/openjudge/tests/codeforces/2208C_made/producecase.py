#!/usr/bin/env python3
"""2208C Stamina and Tasks: exact recursive oracle for small cases."""
from __future__ import annotations
import random
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

SAMPLE = "2\n2\n10 0\n20 5\n3\n10 5\n10 80\n20 5\n"
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed, attempt=0):
    r = random.Random(2208_000_003 + seed * 9176 + attempt); count = (1, 2, 10, 100)[(seed-1)%4]; groups = []
    for index in range(count):
        n = (1, 2, 15, 1000)[(seed+index)%4]
        tasks = [(r.randint(1,100), r.choice((0, 5, 50, 80, 100)) if index % 3 == 0 else r.randint(0,100)) for _ in range(n)]
        groups.append(tasks)
    return str(count)+"\n"+"".join(f"{len(tasks)}\n"+"".join(f"{c} {p}\n" for c,p in tasks) for tasks in groups)


def valid(text):
    v=list(map(int,text.split())); cur=1; total=0
    try:
        for _ in range(v[0]):
            n=v[cur]; tasks=v[cur+1:cur+1+2*n]; cur+=1+2*n; total+=n
            if not 1<=n<=100_000 or len(tasks)!=2*n or not all(1<=x<=100 for x in tasks[::2]) or not all(0<=x<=100 for x in tasks[1::2]): return False
    except IndexError:return False
    return 1<=v[0]<=1000 and cur==len(v) and total<=100_000


def oracle(text):
    v=list(map(int,text.split())); cur=1; answers=[]
    for _ in range(v[0]):
        n=v[cur]; cur+=1; tasks=[tuple(v[cur+i*2:cur+i*2+2]) for i in range(n)]; cur+=2*n
        # Backward recurrence from homogeneity of current stamina.
        value=0.0
        for c,p in reversed(tasks): value=max(value, c+(1-p/100)*value)
        answers.append(f"{value:.10f}")
    return "\n".join(answers)+"\n"


def build():
    out=Path(__file__).with_name("data");out.mkdir(exist_ok=True);cases=[SAMPLE]
    for seed in range(1,21):
        attempt=0;case=generate(seed)
        while case in cases:attempt+=1;case=generate(seed,attempt)
        cases.append(case)
    for index,case in enumerate(cases):
        if not valid(case):raise SystemExit(f"invalid {index}")
        answer=subprocess.run([sys.executable,str(REFERENCE)],input=case,text=True,capture_output=True,check=True).stdout
        if answer!=oracle(case):raise SystemExit(f"oracle disagreement {index}")
        (out/f"{index}.in").write_text(case,encoding="utf-8");(out/f"{index}.out").write_text(answer,encoding="utf-8")


if __name__=="__main__":build()
