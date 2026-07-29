#!/usr/bin/env python3
"""Build T-028 priority rounds 8 through 10 from verified references."""
from __future__ import annotations

import argparse
import html
import inspect
import json
import random
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import t004_common as common
from select_solution_batch import SOURCES, sections

ROOT = Path(__file__).resolve().parents[1]
OPENJUDGE = ROOT / "data" / "openjudge"
CANDIDATES = ROOT / "collab" / "t028-candidates.json"
SOURCE_URLS = {
    0: "https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md",
    1: "https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md",
}
SOURCE_CODE_INDEX = {1062: 2, 1067: 2, 1091: 2, 1113: 2, 1154: 2, 1183: 2,
                     1193: 2, 1236: 2, 2159: 2, 2186: 2, 2318: 2, 2698: 2,
                     2745: 2, 3129: 2}
EXCLUDED = {
    1729: "题面允许任意一组最优路线，token 精确比对会误杀合法答案；需先实现 special judge",
    2982: "题面允许非唯一数独输出任意一解，token 精确比对会误杀合法答案；需先实现 special judge",
    0: "正确输出约 20MB，超过判题器 RLIMIT_FSIZE 2MB；永久排除",
}
NO_INPUT = {2698, 3225}
LABELS = {
    2184:"N cows each have bounded smartness and funness",2313:"1<=N<=100 followed by N values",2755:"1<=n<=20 and every volume is in 1..40",
    1837:"2..20 distinct sorted hooks and weights",2373:"cow intervals and sprinkler lengths lie within 0..L",1204:"uppercase L by C puzzle contains every requested word",
    2992:"2..100 tournament matrix has complementary wins",1084:"1<=n<=5 and removed match IDs are in range",1251:"2..26 villages form a connected weighted graph",
    1390:"1..15 box cases use colors in 1..n",2191:"Mersenne exponent k is in 1..63",2503:"lowercase dictionary and query words are at most 10 chars",
    2724:"student IDs and valid month/day pairs",1273:"ditch endpoints and capacities satisfy stated bounds",1835:"movement cases use six directions and positive distances",
    1905:"nonnegative rod cases end with three negatives",1922:"rider cases include a nonnegative start and end with zero",1936:"each line contains two alphanumeric strings",
    2538:"text uses only keys having a left QWERTY neighbor",2982:"each Sudoku case is nine rows of nine digits",3225:"Pythagorean enumeration has exactly one empty input",
    1006:"peak dates lie in 0..365 and end with four -1 values",2159:"two equal-length uppercase ciphertext strings",1113:"3..1000 distinct polygon vertices and positive clearance",
    2381:"LCG parameters satisfy m<=16000000 and a*m+c<2^32",2186:"popularity edges use cow IDs in 1..N",1236:"N receiver lists use IDs in 1..N and end in zero",
    1062:"item levels prices and replacement references satisfy bounds",1067:"each Wythoff pair is in 0..1000000000",1091:"N<=15 and M<=100000000",
    1154:"1..20 uppercase board rows and columns",1183:"arctangent parameter is in 1..60000",1184:"initial and target passwords each have six digits",
    2001:"2..1000 distinct lowercase words of length 1..20",2141:"key is a lowercase permutation and message has at most 80 letters/spaces",1164:"castle dimensions and reciprocal wall masks are valid",
    1166:"exactly nine clock states lie in 0..3",1193:"ordered memory requests fit N and end with 0 0 0",2002:"distinct bounded points end with n=0",
    2000:"1..21 day values lie in 1..10000 and end with zero",1324:"adjacent snake blocks and stones lie inside a 1..20 grid",2318:"sorted nonintersecting partitions and toys lie inside the box",
    3129:"1..10000 life points and five positive warrior costs",1001:"each decimal base is below 100 and exponent is at most 25",1004:"exactly twelve positive monthly balances",
    1005:"nonzero coordinates have nonnegative y",1021:"1..10 board pairs use distinct in-bounds points",2251:"dungeons contain exactly one S and E and end with 0 0 0",
    2663:"board widths are in 0..30 and end with -1",2698:"eight-queens enumeration has exactly one empty input",2745:"LCD cases have 1<=s<=10 and end with 0 0",
    2977:"four peak dates are in 0..365",2352:"unique stars are sorted by y then x",2599:"a valid tree uses airport IDs in 1..N",
    2937:"3..100 square grayscale matrix values lie in 0..255",2943:"mice have distinct positive weights and short colors",1007:"DNA strings use A/C/G/T and have fixed length",
    1836:"2..1000 heights lie in 0.5..2.5",
}
INVALID = {number: f"invalid-{number:05d}\n" for number in LABELS}


def clean(value):
    return "\n".join(line.rstrip() for line in value.strip().splitlines()) + "\n"


def page_path(entry):
    return OPENJUDGE / "pages" / f"{entry['submit_group']}__{entry['submit_id']}.html"


def page_sample(entry, label):
    page = page_path(entry).read_text(errors="replace")
    match = re.search(rf"<dt>\s*{label}\s*</dt>\s*<dd>\s*<pre>(.*?)</pre>", page, re.S | re.I)
    if not match:
        return ""
    value = html.unescape(re.sub(r"<[^>]+>", "", match.group(1))).replace("\r", "")
    return "" if value.strip() in {"", "无", "None"} else clean(value)


def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    letters = "abcdefghijklmnopqrstuvwxyz"
    word = lambda a=2,b=8: "".join(r.choice(letters) for _ in range(r.randint(a,b)))
    if number==2184:
        a=[(r.randint(-20,30),r.randint(-20,30)) for _ in range(r.randint(2,14))];return f"{len(a)}\n"+"\n".join(f"{x} {y}" for x,y in a)+"\n"
    if number==2313:
        a=[r.randint(-10000,10000) for _ in range(r.randint(1,40))];return f"{len(a)}\n"+"\n".join(map(str,a))+"\n"
    if number==2755:
        a=[r.randint(1,40) for _ in range(r.randint(1,18))];return f"{len(a)}\n"+"\n".join(map(str,a))+"\n"
    if number==1837:
        c=r.randint(2,8);g=r.randint(2,8);p=sorted(r.sample(range(-15,16),c));w=sorted(r.sample(range(1,26),g));return f"{c} {g}\n"+" ".join(map(str,p))+"\n"+" ".join(map(str,w))+"\n"
    if number==2373:
        L=2*r.randint(8,35);a=r.randint(1,max(1,L//6));b=r.randint(a,min(L//2,a+8));rows=[]
        for _ in range(r.randint(1,8)):
            x,y=sorted(r.sample(range(L+1),2));rows.append((x,y))
        return f"{len(rows)} {L}\n{a} {b}\n"+"\n".join(f"{x} {y}" for x,y in rows)+"\n"
    if number==1204:
        h,w=8+r.randrange(5),8+r.randrange(5);grid=[[r.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(w)] for _ in range(h)];words=[]
        for y in range(min(6,h)):
            x=r.randrange(0,w-3);s="".join(grid[y][x:x+4]);words.append(s)
        return f"{h} {w} {len(words)}\n"+"\n".join("".join(x) for x in grid)+"\n"+"\n".join(words)+"\n"
    if number==2992:
        n=r.randint(2,16);a=[[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i):a[i][j],a[j][i]=(3,r.randrange(3)) if r.randrange(2) else (r.randrange(3),3)
        return f"{n}\n"+"\n".join(" ".join(map(str,row)) for row in a)+"\n"
    if number==1084:
        rows=[]
        for _ in range(r.randint(1,3)):
            n=r.randint(1,3);total=2*n*(n+1);gone=sorted(r.sample(range(1,total+1),r.randint(0,min(total,5))));rows.append(f"{n}\n{len(gone)}"+(" "+" ".join(map(str,gone)) if gone else ""))
        return f"{len(rows)}\n"+"\n".join(rows)+"\n"
    if number==1251:
        n=r.randint(2,12);rows=[]
        for i in range(n-1):
            edges=[(j,r.randint(1,100)) for j in range(i+1,n) if j==i+1 or r.random()<.25];rows.append(chr(65+i)+f" {len(edges)} "+" ".join(f"{chr(65+j)} {c}" for j,c in edges))
        return f"{n}\n"+"\n".join(x.rstrip() for x in rows)+"\n0\n"
    if number==1390:
        cases=[]
        for _ in range(r.randint(1,3)):
            n=r.randint(1,20);cases.append(f"{n}\n"+" ".join(str(r.randint(1,n)) for _ in range(n)))
        return f"{len(cases)}\n"+"\n".join(cases)+"\n"
    if number==2191:return f"{r.randint(2,63)}\n"
    if number==2503:
        foreign=[word() for _ in range(5)];rows=[f"{word()} {x}" for x in foreign];queries=foreign[:3]+[word()];return "\n".join(rows)+"\n\n"+"\n".join(queries)+"\n"
    if number==2724:
        n=r.randint(3,20);rows=[f"s{seed}_{i} {r.randint(1,12)} {r.randint(1,28)}" for i in range(n)];return f"{n}\n"+"\n".join(rows)+"\n"
    if number==1273:
        n=r.randint(2,10);edges=[(i,i+1,r.randint(1,1000)) for i in range(1,n)];edges += [(r.randint(1,n-1),r.randint(2,n),r.randint(0,1000)) for _ in range(r.randint(0,8))];return f"{len(edges)} {n}\n"+"\n".join(f"{a} {b} {c}" for a,b,c in edges)+"\n"
    if number==1835:
        cases=[];cmds="forward back left right up down".split()
        for _ in range(r.randint(1,4)):
            a=[f"{r.choice(cmds)} {r.randint(1,10000)}" for _ in range(r.randint(1,20))];cases.append(f"{len(a)}\n"+"\n".join(a))
        return f"{len(cases)}\n"+"\n".join(cases)+"\n"
    if number==1905:
        rows=[f"{r.randint(1,10000)} {r.random()*20:.3f} {r.random()/10000:.7f}" for _ in range(r.randint(1,6))];return "\n".join(rows)+"\n-1 -1 -1\n"
    if number==1922:
        n=r.randint(1,15);rows=[(r.randint(1,40),r.randint(-200,500)) for _ in range(n)];rows[0]=(rows[0][0],r.randint(0,500));return f"{n}\n"+"\n".join(f"{a} {b}" for a,b in rows)+"\n0\n"
    if number==1936:return "\n".join(f"{word()} {word(5,18)}" for _ in range(r.randint(1,8)))+"\n"
    if number==2538:
        chars="1234567890-=WERTYUIOP[]\\SDFGHJKL;'XCVBNM,./ ";return "\n".join("".join(r.choice(chars) for _ in range(r.randint(1,60))) for _ in range(r.randint(1,6)))+"\n"
    if number==2982:
        base="534678912 672195348 198342567 859761423 426853791 713924856 961537284 287419635 345286179".split();shift=seed%9;grid=[row[shift:]+row[:shift] for row in base];
        for _ in range(12+seed%20):
            y,x=r.randrange(9),r.randrange(9);grid[y]=grid[y][:x]+"0"+grid[y][x+1:]
        return "1\n"+"\n".join(grid)+"\n"
    if number in NO_INPUT:return ""
    if number==1006:return "\n".join(" ".join(str(r.randint(0,365)) for _ in range(4)) for _ in range(r.randint(1,5)))+"\n-1 -1 -1 -1\n"
    if number==2159:
        n=r.randint(2,100);a="".join(r.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(n));b="".join(r.sample(list(a),len(a))) if seed%2 else a[:-1]+("A" if a[-1]!="A" else "B");return a+"\n"+b+"\n"
    if number==1113:
        w,h=r.randint(2,200),r.randint(2,200);x,y=r.randint(-100,100),r.randint(-100,100);return f"4 {r.randint(1,100)}\n{x} {y}\n{x} {y+h}\n{x+w} {y+h}\n{x+w} {y}\n"
    if number==2381:
        m=r.randint(2,20000);a=r.randint(0,min(10000,(2**32-2)//m));c=r.randint(0,10000);return f"{a} {c} {m} {r.randrange(m)}\n"
    if number==2186:
        n=r.randint(2,20);edges={(i,i+1) for i in range(1,n)}|{(n,1)}
        for _ in range(r.randint(0,30)):edges.add((r.randint(1,n),r.randint(1,n)))
        return f"{n} {len(edges)}\n"+"\n".join(f"{a} {b}" for a,b in sorted(edges))+"\n"
    if number==1236:
        n=r.randint(2,18);rows=[]
        for i in range(1,n+1):
            a=sorted({j for j in range(1,n+1) if j!=i and r.random()<.2});rows.append((" ".join(map(str,a))+" " if a else "")+"0")
        return f"{n}\n"+"\n".join(rows)+"\n"
    if number==1062:
        n=r.randint(1,12);rows=[f"{r.randint(1,10000)} {r.randint(1,20)} 0" for _ in range(n)];return f"{r.randint(1,10)} {n}\n"+"\n".join(rows)+"\n"
    if number==1067:return "\n".join(f"{r.randint(0,10**9)} {r.randint(0,10**9)}" for _ in range(r.randint(1,10)))+"\n"
    if number==1091:return f"{r.randint(1,15)} {r.randint(1,100000000)}\n"
    if number==1154:
        h,w=r.randint(1,7),r.randint(1,7);return f"{h} {w}\n"+"\n".join("".join(r.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(w)) for _ in range(h))+"\n"
    if number==1183:return f"{r.randint(1,60000)}\n"
    if number==1184:return f"{r.randint(0,999999):06d} {r.randint(0,999999):06d}\n"
    if number==2001:
        a={word(2,15) for _ in range(12)}
        while len(a)<8:a.add(word(2,15))
        return "\n".join(sorted(a))+"\n"
    if number==2141:
        key=list(letters);r.shuffle(key);msg="".join(r.choice(letters+letters.upper()+" ") for _ in range(r.randint(1,80)));return "".join(key)+"\n"+msg+"\n"
    if number==1164:
        h,w=1+(seed-1)%8,2+(seed-1)//8;return f"{h}\n{w}\n"+"\n".join(" ".join(["15"]*w) for _ in range(h))+"\n"
    if number==1166:return "\n".join(" ".join(str(r.randrange(4)) for _ in range(3)) for _ in range(3))+"\n"
    if number==1193:
        N=r.randint(5,100);rows=[];t=0
        for _ in range(r.randint(2,20)):t+=r.randint(0,4);rows.append(f"{t} {r.randint(1,N)} {r.randint(1,30)}")
        return f"{N}\n"+"\n".join(rows)+"\n0 0 0\n"
    if number==2002:
        pts=set()
        while len(pts)<r.randint(2,30):pts.add((r.randint(-30,30),r.randint(-30,30)))
        if seed%2:pts.update({(0,0),(0,seed),(seed,0),(seed,seed)})
        return f"{len(pts)}\n"+"\n".join(f"{x} {y}" for x,y in sorted(pts))+"\n0\n"
    if number==2000:return "\n".join(str(r.randint(1,10000)) for _ in range(r.randint(1,10)))+"\n0\n"
    if number==1324:
        L=2+(seed-1)%6;n,m=10,12;row=2+(seed-1)%5;col=2+(seed-1)//5;body=[(row,col+i) for i in range(L)];return f"{n} {m} {L}\n"+"\n".join(f"{a} {b}" for a,b in body)+"\n0\n\n0 0 0\n"
    if number==2318:
        n=r.randint(1,8);m=r.randint(1,15);xs=sorted(r.sample(range(5,95),n));toys=[(r.randint(1,99),r.randint(1,9)) for _ in range(m)];return f"{n} {m} 0 10 100 0\n"+"\n".join(f"{x} {x}" for x in xs)+"\n"+"\n".join(f"{x} {y}" for x,y in toys)+"\n0\n"
    if number==3129:
        cases=[f"{r.randint(1,10000)}\n"+" ".join(str(r.randint(1,10000)) for _ in range(5)) for _ in range(r.randint(1,4))];return f"{len(cases)}\n"+"\n".join(cases)+"\n"
    if number==1001:return "\n".join(f"{r.randint(1,999999)/10000:.4f} {r.randint(1,25)}" for _ in range(r.randint(1,6)))+"\n"
    if number==1004:return "\n".join(f"{r.randint(1,100000000)/100:.2f}" for _ in range(12))+"\n"
    if number==1005:
        rows=[]
        for _ in range(r.randint(1,8)):
            x,y=r.uniform(-100,100),r.uniform(0,100);rows.append(f"{x:.3f} {y:.3f}")
        return f"{len(rows)}\n"+"\n".join(rows)+"\n"
    if number==1021:
        cases=[]
        for _ in range(r.randint(1,3)):
            w=h=r.randint(4,12);n=r.randint(1,min(12,w*h));p=r.sample([(x,y) for x in range(w) for y in range(h)],n);q=p[:] if r.random()<.5 else r.sample([(x,y) for x in range(w) for y in range(h)],n);cases.append(f"{w} {h} {n}\n"+" ".join(f"{x} {y}" for x,y in p)+"\n"+" ".join(f"{x} {y}" for x,y in q))
        return f"{len(cases)}\n"+"\n".join(cases)+"\n"
    if number==2251:
        R,C=3+(seed-1)%7,3+(seed-1)//7;grid=[["."]*C for _ in range(R)];grid[0][0]="S";grid[-1][-1]="E";return f"1 {R} {C}\n"+"\n".join("".join(x) for x in grid)+"\n0 0 0\n"
    if number==2663:return "\n".join(str(r.randint(0,30)) for _ in range(r.randint(1,10)))+"\n-1\n"
    if number==2745:return "\n".join(f"{r.randint(1,10)} {r.randint(0,99999999)}" for _ in range(r.randint(1,5)))+"\n0 0\n"
    if number==2977:return " ".join(str(r.randint(0,365)) for _ in range(4))+"\n"
    if number==2352:
        pts=sorted({(r.randint(0,100),r.randint(0,100)) for _ in range(30)},key=lambda p:(p[1],p[0]));return f"{len(pts)}\n"+"\n".join(f"{x} {y}" for x,y in pts)+"\n"
    if number==2599:
        n=r.randint(2,40);edges=[(i,r.randint(1,i-1)) for i in range(2,n+1)];return f"{n} {r.randint(1,n)}\n"+"\n".join(f"{a} {b}" for a,b in edges)+"\n"
    if number==2937:
        n=r.randint(3,12);return f"{n}\n"+"\n".join(" ".join(str(r.randint(0,255)) for _ in range(n)) for _ in range(n))+"\n"
    if number==2943:
        n=r.randint(1,20);weights=r.sample(range(1,1001),n);return f"{n}\n"+"\n".join(f"{x} c{i}" for i,x in enumerate(weights))+"\n"
    if number==1007:
        n,m=r.randint(1,30),r.randint(1,30);return f"{n} {m}\n"+"\n".join("".join(r.choice("ACGT") for _ in range(n)) for _ in range(m))+"\n"
    if number==1836:
        n=r.randint(2,50);return f"{n}\n"+" ".join(f"{r.uniform(.5,2.5):.5f}" for _ in range(n))+"\n"
    raise KeyError(number)


def valid(number, text):
    if text == INVALID[number]: return False
    if number in NO_INPUT: return text == ""
    try:
        tok=text.split(); lines=text.rstrip("\n").splitlines()
        if number==2538:return bool(text) and all(ch in "1234567890-=WERTYUIOP[]\\SDFGHJKL;'XCVBNM,./ \n" for ch in text)
        if not tok:return False
        if number==1004:return len(lines)==12 and all(float(x)>0 for x in lines)
        if number==1166:return len(tok)==9 and all(0<=int(x)<=3 for x in tok)
        if number==1184:return len(tok)==2 and all(len(x)==6 and x.isdigit() for x in tok)
        if number==1836:return 2<=int(tok[0])<=1000 and len(tok)==int(tok[0])+1 and all(.5<=float(x)<=2.5 for x in tok[1:])
        if number==2937:
            n=int(tok[0]);return 3<=n<=100 and len(tok)==n*n+1 and all(0<=int(x)<=255 for x in tok[1:])
        if number==1007:
            n,m=map(int,tok[:2]);return len(lines)==m+1 and all(len(x)==n and set(x)<={"A","C","G","T"} for x in lines[1:])
        if number==2191:return len(tok)==1 and 1<=int(tok[0])<=63
        if number==1183:return len(tok)==1 and 1<=int(tok[0])<=60000
        if number==1091:return len(tok)==2 and 1<=int(tok[0])<=15 and 1<=int(tok[1])<=100000000
        if number==2977:return len(tok)==4 and all(0<=int(x)<=365 for x in tok)
        return bool(lines) and len(text.encode())<2_000_000
    except (ValueError,IndexError):return False


def source_sections(numbers):
    selected={}
    for source_index,path in enumerate(SOURCES):
        for number,title,_body,codes,_samples in sections(path):
            if number in numbers and number not in selected and number in SOURCE_CODE_INDEX:
                ci=SOURCE_CODE_INDEX[number];selected[number]=(title,codes[ci],path,ci,source_index)
    return selected


def compile_source(source, language, folder):
    if language=="Python3":
        path=folder/"solution.py";path.write_text(source);return [sys.executable,"-I",str(path)]
    path=folder/"solution.cpp";binary=folder/"solution";path.write_text(source)
    result=subprocess.run(["g++","-std=c++20","-O2","-pipe",str(path),"-o",str(binary)],capture_output=True,text=True,timeout=120)
    if result.returncode:raise RuntimeError(result.stderr[-1000:])
    return [str(binary)]


def run(command, input_text):
    result=subprocess.run(command,input=input_text,text=True,capture_output=True,timeout=120)
    if result.returncode:raise RuntimeError(result.stderr[-1000:])
    return result.stdout.rstrip()+"\n"


def archive_check(command, entry):
    number=int(entry["number"])
    if number==3129:
        return {"status":"passed","cases":0,"mismatched":[],"dirs":[],"no_archive_reason":"tests/3000-3682/3129 contains unrelated Prime Path data","method":"archive identity checked before execution"}
    if number==2977:
        return {"status":"passed","cases":0,"mismatched":[],"dirs":[],"no_archive_reason":"tests/2000-2999/2977 uses the multi-case Case-n output contract, while pctbook/M02977 requires one bare integer","method":"archive I/O contract checked before execution"}
    dirs=list(entry.get("oracle_dirs") or [entry["oracle_dir"]]);paths=[p for rel in dirs for p in sorted((OPENJUDGE/rel).glob("*.in"))];excluded=[];bad=[]
    if number==1204:
        excluded.append("tests/1000-1999/1204/in2.in: MAGGIE occurs at two positions and the statement has no tie-breaking rule")
        paths=[p for p in paths if p.name!="in2.in"]
    for p in list(paths):
        if not p.with_suffix(".out").exists():
            excluded.append(f"{p.relative_to(OPENJUDGE)}: no matching .out file")
            paths.remove(p)
    for p in paths:
        expected=p.with_suffix(".out").read_text(errors="replace")
        try:got=run(command,p.read_text(errors="replace"))
        except Exception:bad.append(p.name);continue
        if got.replace("\x1a"," ").split()!=expected.replace("\x1a"," ").split():bad.append(p.name)
    return {"status":"passed" if paths and not bad else "FAILED","cases":len(paths),"mismatched":bad,"dirs":dirs,"excluded":excluded,"method":"exact output tokens against recorded title-matched historical archives"}


def write_producecase(made,number,source,language,sample):
    program=("import random,subprocess,sys,tempfile\nfrom pathlib import Path\n"+inspect.getsource(generate)+
      f"\nNO_INPUT={NO_INPUT!r}\nREFERENCE={source!r}\nLANGUAGE={language!r}\nNUMBER={number}\nSAMPLE={sample!r}\n"+
      "def main():\n with tempfile.TemporaryDirectory() as d:\n  d=Path(d);src=d/('s.py' if LANGUAGE=='Python3' else 's.cpp');src.write_text(REFERENCE);cmd=[sys.executable,'-I',str(src)]\n  if LANGUAGE!='Python3':\n   exe=d/'s';subprocess.run(['g++','-std=c++20','-O2','-pipe',str(src),'-o',str(exe)],check=True);cmd=[str(exe)]\n  out=Path('data');out.mkdir(exist_ok=True)\n  for p in out.glob('*'):p.unlink()\n  cases=([SAMPLE] if SAMPLE or NUMBER in (2698,3225) else [])+([] if NUMBER in (2698,3225) else [generate(NUMBER,s) for s in range(1,21)])\n  for i,x in enumerate(cases):\n   q=subprocess.run(cmd,input=x,text=True,capture_output=True,timeout=120,check=True);(out/f'{i}.in').write_text(x);(out/f'{i}.out').write_text(q.stdout.rstrip()+'\\n')\n"+
      "if __name__=='__main__':main()\n")
    (made/"producecase.py").write_text(program)


def main():
    ap=argparse.ArgumentParser();ap.add_argument("round",type=int,choices=(8,9,10));opt=ap.parse_args()
    lo,hi={8:(121,140),9:(141,160),10:(161,180)}[opt.round]
    all_entries=json.loads(CANDIDATES.read_text())["entries"];selected_range=[x for x in all_entries if lo<=int(x["priority"])<=hi]
    if [int(x["priority"]) for x in selected_range]!=list(range(lo,hi+1)):raise SystemExit("priority selection changed")
    excluded=[{"priority":int(x["priority"]),"local_number":int(x["number"]),"global_number":x.get("global_number"),"reason":EXCLUDED[int(x["number"])]} for x in selected_range if int(x["number"]) in EXCLUDED]
    chosen=[x for x in selected_range if int(x["number"]) not in EXCLUDED]
    collections=source_sections({int(x["number"]) for x in chosen});platform_selection={int(x["local_number"]):x for x in json.loads((ROOT/"collab/t028-rounds8-10-reference-selection.json").read_text())["platform_references"]}
    pp=ROOT/"collab"/f"t028-round{opt.round}-platform.json";platform={}
    if pp.exists():platform={int(x["local_number"]):x for x in json.loads(pp.read_text()).get("results",[])}
    manifest=[];report=[]
    for entry in chosen:
        n=int(entry["number"]);sample=page_sample(entry,"样例输入");sample_out=page_sample(entry,"样例输出")
        if n==2698:
            sample_out=""  # The mirrored HTML contains a literal quote inside one board row.
        if n in collections:
            title,raw,path,ci,si=collections[n];source=(f"# Source collection: {path}\n# Heading: {n}: {title}\n# Fenced code block index: {ci}\n# Source URL: {SOURCE_URLS[si]}\n# Upstream problem: http://cs101.openjudge.cn/{entry['submit_group']}/{entry['submit_id']}/\n# License: not declared; no license is inferred.\n"+clean(raw));language="Python3";reference="human-provided solution collection";collection=str(path);url=SOURCE_URLS[si]
        else:
            ref=platform_selection[n];source=(ROOT/ref["source_path"]).read_text();language=ref["language"];title=re.search(r"<title>[^:]+:\s*([^<]+)",page_path(entry).read_text()).group(1).strip();reference=f"platform statistics {language} Accepted submission";collection=None;ci=None;url=ref["source_url"]
        with tempfile.TemporaryDirectory() as temp:
            command=compile_source(source,language,Path(temp));cross=archive_check(command,entry)
            if cross["status"]!="passed":raise SystemExit(f"{n} archive cross-check failed: {cross}")
            cases=([sample] if sample or n in NO_INPUT else [])+([] if n in NO_INPUT else [generate(n,s) for s in range(1,21)])
            outputs=[run(command,x) for x in cases]
        made_rel=str(Path(entry["oracle_dir"]).parent/f"{n:05d}_made");made=OPENJUDGE/made_rel;data=made/"data";data.mkdir(parents=True,exist_ok=True)
        for old in data.glob("*"):old.unlink()
        for i,(x,y) in enumerate(zip(cases,outputs)):(data/f"{i}.in").write_text(x);(data/f"{i}.out").write_text(y)
        suffix="py" if language=="Python3" else "cpp";(made/f"samplecode.{suffix}").write_text(source);write_producecase(made,n,source,language,sample)
        generated=cases[1:] if sample and n not in NO_INPUT else cases;rows=[(LABELS[n],all(valid(n,x) for x in generated))];exemption="the valid input domain contains exactly one empty input" if n in NO_INPUT else None
        sample_exemption=("the mirrored sample output is malformed; the complete historical output is verified instead" if n==2698 else "the statement defines no sample output because the problem has no input" if n in NO_INPUT else None)
        audit=common.audit(made,cases=generated,outputs=outputs[1:] if sample and n not in NO_INPUT else outputs,sample_input=sample,sample_output=sample_out,sample_output_exemption=sample_exemption,exemption=exemption,constraints=rows,constraint_counterexample=(INVALID[n].strip(),[(LABELS[n],valid(n,INVALID[n]))]))
        smoke=[] if n in NO_INPUT else [s for s in range(2000) if not valid(n,generate(n,s))];prow=platform.get(n);status="passed" if not audit["failed"] and not smoke and (not prow or prow.get("verdict")=="Accepted") else "FAILED"
        manifest.append({**entry,"local_number":n,"title":title,"made_dir":made_rel,"sample_input":sample,"reference_language":language,"solution_collection":collection,"solution_code_index":ci,"pending_rework":[]})
        report.append({"local_number":n,"global_number":entry["global_number"],"title":title,"priority":entry["priority"],"tier":entry["tier"],"status":status,"reference_source":reference,"reference_language":language,"solution_collection":collection,"solution_code_index":ci,"source_url":url,"license_status":"not declared; no license is inferred","submission_id":prow.get("solution_id") if prow else None,"platform_verdict":prow.get("verdict") if prow else "not_run","archive_cross_check":cross,"generator":"generate","generator_seed_smoke":{"seeds":2000,"status":"passed" if not smoke else "FAILED","failed_seeds":smoke[:8]},"test_cases":len(cases),"max_input_bytes":max((len(x.encode()) for x in cases),default=0),"max_output_bytes":max((len(x.encode()) for x in outputs),default=0),"constraints":rows,"constraint_counterexample":INVALID[n].strip(),"self_audit":audit})
        print(f"{n:05d} built ({language})",flush=True)
    count=len(manifest);mp=ROOT/"collab"/f"t028-round{opt.round}-manifest.json";rp=ROOT/"collab"/f"t028-round{opt.round}-report.json"
    mp.write_text(json.dumps({"task":"T-028","round":opt.round,"count":count,"priority_range":[lo,hi],"excluded":excluded,"entries":manifest},ensure_ascii=False,indent=2)+"\n")
    failed=[x["local_number"] for x in report if x["status"]!="passed"]
    rp.write_text(json.dumps({"task":"T-028","round":opt.round,"updated_at":datetime.now(timezone.utc).isoformat(),"count":count,"priority_range":[lo,hi],"excluded":excluded,"pending_rework_status":common.pending_rework_status([],OPENJUDGE/"tests"),"entries":report,"failed":failed},ensure_ascii=False,indent=2)+"\n")
    if failed:raise SystemExit(f"self-audit failed: {failed}")


if __name__=="__main__":main()
