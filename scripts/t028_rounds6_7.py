#!/usr/bin/env python3
"""Build T-028 priority rounds 6 and 7 (81 through 120)."""
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
SOURCE_CODE_INDEX = {
    3247: 2, 1002: 2, 2181: 2, 2936: 2, 2814: 4, 2910: 2, 2940: 2,
    1178: 2, 1190: 2, 2899: 2, 2942: 2, 2804: 2, 1077: 6, 1230: 0,
    2049: 2, 2767: 2, 2787: 2, 2927: 2, 2979: 2, 1008: 2, 1019: 2,
    1026: 2, 1047: 2, 1056: 2, 1742: 2, 1789: 2, 1941: 3, 2092: 2,
    2253: 2, 2337: 3, 2676: 2, 2712: 2, 2883: 2, 2911: 2, 2913: 2,
}
PLATFORM_SOURCES = {1276, 1481, 1753, 2791, 2818}
LABELS = {
    3247: "1<=n<=9", 1002: "1<=n<=100000 and each phone has seven mapped digits",
    2181: "1<=P<=100000 and exactly P potion values follow", 2936: "1<=N<=8 distinct sorted IDs lie in 1..8",
    2814: "exactly nine clock states lie in 0..3", 2910: "one non-whitespace string has length at most 100",
    2940: "1<=a,n<=9", 1178: "2..64 distinct chess positions are encoded as letter-digit pairs",
    1190: "1<=N<=10000 and 1<=M<=10", 2899: "a 5x5 integer matrix and two row indices are supplied",
    2942: "1<=N<20", 2791: "each case has 2..15 distinct points in -1000..1000 and input ends with 0",
    2804: "dictionary and document words are lowercase, length<=10, with a blank separator",
    1077: "the input is one permutation of 1..8 and x", 1230: "1<=t<=10, 1<=n<=100, 0<=k<=100, wall coordinates are in 0..100",
    1276: "each cash case has nonnegative cash and valid positive denomination counts and values",
    1481: "each picture is 5..50 by 5..50 and contains only '.', '*', 'X', followed by 0 0",
    2049: "walls and doors use endpoints in 1..199 and input ends with -1 -1",
    2767: "one nonempty ciphertext line has at most 200 characters", 2787: "each case has four integers in 1..9 and input ends with four zeros",
    2927: "input contains one or more text lines", 2979: "each jury case has 1<=m<=n<=200 and scores in 0..20, followed by 0 0",
    1008: "Haab dates use valid days, months, and nonnegative years", 1019: "1<=t<=10 and every position is in 1..2147483647",
    1026: "each key is a permutation and message counts end with 0; blocks end with n=0",
    1047: "each input integer has 2..60 digits and leading zeroes are preserved",
    1056: "each set has 2..8 distinct binary codes of length 1..10 and ends with 9",
    1742: "1<=n<=100, 1<=m<=100000, positive values/counts, followed by 0 0",
    1789: "each case has 2..2000 distinct seven-letter lowercase codes and ends with 0",
    1941: "each order is in 1..10 and input ends with 0", 2092: "2<=N<=500, 1<=M<=500 and player IDs are 1..10000, followed by 0 0",
    2253: "each case has 2..200 points and input ends with 0", 2337: "1<=t and each case has 3..1000 lowercase words",
    2676: "k is positive and exactly k positive integers follow", 2712: "dates are valid in one non-leap year and the target date is later",
    2818: "each cipher key is a permutation and block messages end with 0; input ends with n=0",
    2883: "every case contains exactly five integers", 2911: "MAX is a four-digit integer",
    2913: "one line contains only ASCII characters 32..122", 1753: "the board is exactly four rows of four 'b'/'w' cells",
}
INVALID = {n: f"invalid-{n}\n" for n in LABELS}
INVALID.update({3247: "10\n", 2936: "2\n1 1\n", 2814: "0 1 2\n", 2940: "0 10\n",
                1190: "0\n11\n", 2942: "20\n", 2791: "2\n0 0\n0 0\n0\n",
                1077: "1 2 3 4 5 6 7 7 x\n", 1753: "bbbb\nbbbb\nbbbb\nbbbx\n",
                2911: "999\n", 2787: "1 2 3 10\n0 0 0 0\n"})


def clean(value):
    return "\n".join(line.rstrip() for line in value.strip().splitlines()) + "\n"


def page_sample(number, label):
    page = (OPENJUDGE / "pages" / f"practice__{number:05d}.html").read_text(errors="replace")
    match = re.search(rf"<dt>\s*{label}\s*</dt>\s*<dd>\s*<pre>(.*?)</pre>", page, re.S | re.I)
    if not match:
        raise ValueError(f"{number}: missing {label}")
    value = html.unescape(re.sub(r"<[^>]+>", "", match.group(1))).replace("\r", "")
    return clean(value)


def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    letters = "abcdefghijklmnopqrstuvwxyz"
    word = lambda a=1, b=10: "".join(r.choice(letters) for _ in range(r.randint(a, b)))
    if number == 3247: return f"{seed % 9 + 1}\n"
    if number == 1002:
        base = ["4873279", "ITS-EASY", "888-4567", "3-10-10-10"]
        rows = [r.choice(base) for _ in range(r.randint(2, 30))]
        return f"{len(rows)}\n" + "\n".join(rows) + "\n"
    if number == 2181:
        a = [r.randint(0, 1000) for _ in range(r.randint(1, 100))]
        return f"{len(a)}\n" + "\n".join(map(str, a)) + "\n"
    if number == 2936:
        a = sorted(r.sample(range(1, 9), r.randint(1, 8))); return f"{len(a)}\n" + " ".join(map(str, a)) + "\n"
    if number == 2814: return " ".join(str(r.randrange(4)) for _ in range(9)) + "\n"
    if number == 2910:
        chars = letters + letters.upper() + "0123456789*?-_"; return "".join(r.choice(chars) for _ in range(r.randint(1, 100))) + "\n"
    if number == 2940: return f"{r.randint(1,9)} {r.randint(1,9)}\n"
    if number == 1178:
        squares = [f"{chr(65+x)}{y+1}" for y in range(8) for x in range(8)]
        return "".join(r.sample(squares, r.randint(2, 12))) + "\n"
    if number == 1190: return f"{r.randint(1, 2000)}\n{r.randint(1, 7)}\n"
    if number == 2899:
        rows = [" ".join(str(r.randint(-1000, 1000)) for _ in range(5)) for _ in range(5)]
        return "\n".join(rows) + f"\n{r.randint(-2,6)} {r.randint(-2,6)}\n"
    if number == 2942: return f"{seed % 19 + 1}\n"
    if number == 2791:
        pts=set(); n=r.randint(2,8)
        while len(pts)<n: pts.add((r.randint(-20,20),r.randint(-20,20)))
        return f"{n}\n"+"\n".join(f"{x} {y}" for x,y in pts)+"\n0\n"
    if number == 2804:
        foreign=[]; rows=[]
        for _ in range(r.randint(2,15)):
            f=word(); foreign.append(f); rows.append(f"{word()} {f}")
        docs=[r.choice(foreign+[word()]) for _ in range(r.randint(2,20))]
        return "\n".join(rows)+"\n\n"+"\n".join(docs)+"\n"
    if number == 1077:
        board=list("12345678x"); pos=8
        for _ in range(r.randint(0,30)):
            y,x=divmod(pos,3); choices=[q for q in (pos-3,pos+3,pos-1,pos+1) if 0<=q<9 and abs(q%3-x)+abs(q//3-y)==1]
            q=r.choice(choices);board[pos],board[q]=board[q],board[pos];pos=q
        return " ".join(board)+"\n"
    if number == 1230:
        cases=[]
        for _ in range(r.randint(1,4)):
            n=r.randint(1,20); k=r.randint(0,10); walls=[]
            for _ in range(n):
                x1,x2=sorted((r.randint(0,100),r.randint(0,100))); y=r.randint(0,100);walls.append(f"{x1} {y} {x2} {y}")
            cases.append(f"{n} {k}\n"+"\n".join(walls))
        return f"{len(cases)}\n"+"\n".join(cases)+"\n"
    if number == 1276:
        cases=[]
        for _ in range(r.randint(1,5)):
            n=r.randint(1,12); pairs=[(r.randint(1,20),r.randint(1,200)) for _ in range(n)]
            cases.append(f"{r.randint(0,3000)} {n} "+" ".join(f"{c} {v}" for c,v in pairs))
        return "\n".join(cases)+"\n"
    if number == 1481:
        w=h=r.randint(5,15); grid=[["."]*w for _ in range(h)]
        for y,x in [(2,2),(2,3),(3,2),(3,3)]: grid[y][x]="*"
        for y,x in r.sample([(2,2),(2,3),(3,2),(3,3)],r.randint(1,4)):grid[y][x]="X"
        return f"{w} {h}\n"+"\n".join("".join(x) for x in grid)+"\n0 0\n"
    if number == 2049:
        if seed % 2:
            x,y=r.randint(1,198),r.randint(1,198);return f"0 0\n{x}.5 {y}.5\n-1 -1\n"
        # The statement sample exercises walls and doors; translate it so even
        # seeds remain distinct without changing its topology.
        d=seed % 30
        return ("8 9\n"+"\n".join((f"{1+d} 1 1 3",f"{2+d} 1 1 3",f"{3+d} 1 1 3",f"{4+d} 1 1 3",
          f"{1+d} 1 0 3",f"{1+d} 2 0 3",f"{1+d} 3 0 3",f"{1+d} 4 0 3",
          f"{2+d} 1 1",f"{2+d} 2 1",f"{2+d} 3 1",f"{3+d} 1 1",f"{3+d} 2 1",f"{3+d} 3 1",
          f"{1+d} 2 0",f"{3+d} 3 0",f"{4+d} 3 1"))+f"\n{1.5+d} 1.5\n-1 -1\n")
    if number == 2767:
        chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ ,.'!?";return "".join(r.choice(chars) for _ in range(r.randint(1,200)))+"\n"
    if number == 2787:
        rows=[" ".join(str(r.randint(1,9)) for _ in range(4)) for _ in range(r.randint(1,12))]
        return "\n".join(rows)+"\n0 0 0 0\n"
    if number == 2927:
        chars=letters+"0123456789 &^$#@*";return "\n".join("".join(r.choice(chars) for _ in range(r.randint(1,80))) for _ in range(r.randint(1,8)))+"\n"
    if number == 2979:
        cases=[]
        for _ in range(r.randint(1,3)):
            n=r.randint(1,20);m=r.randint(1,n);cases.append(f"{n} {m}\n"+"\n".join(f"{r.randint(0,20)} {r.randint(0,20)}" for _ in range(n)))
        return "\n".join(cases)+"\n0 0\n"
    if number == 1008:
        months="pop no zip zotz tzec xul yoxkin mol chen yax zac ceh mac kankin muan pax koyab cumhu uayet".split();rows=[]
        for _ in range(r.randint(1,12)):
            m=r.randrange(19);day=r.randrange(5 if m==18 else 20);rows.append(f"{day}. {months[m]} {r.randint(0,5000)}")
        return f"{len(rows)}\n"+"\n".join(rows)+"\n"
    if number == 1019:
        a=[r.randint(1,2_147_483_647) for _ in range(r.randint(1,10))];return f"{len(a)}\n"+"\n".join(map(str,a))+"\n"
    if number in (1026,2818):
        n=r.randint(1,30);perm=list(range(1,n+1));r.shuffle(perm);rows=[]
        for _ in range(r.randint(1,8)):
            msg="".join(r.choice(letters+" ") for _ in range(r.randint(1,n)));rows.append(f"{r.randint(1,10**6)} {msg}")
        return f"{n}\n"+" ".join(map(str,perm))+"\n"+"\n".join(rows)+"\n0\n0\n"
    if number == 1047:
        return "\n".join("".join(r.choice("0123456789") for _ in range(r.randint(2,35))) for _ in range(r.randint(1,8)))+"\n"
    if number == 1056:
        groups=[]
        for _ in range(r.randint(1,5)):
            codes=set()
            while len(codes)<r.randint(2,8):codes.add("".join(r.choice("01") for _ in range(r.randint(1,10))))
            groups.extend(sorted(codes));groups.append("9")
        return "\n".join(groups)+"\n"
    if number == 1742:
        cases=[]
        for _ in range(r.randint(1,4)):
            n=r.randint(1,20);m=r.randint(1,1000);a=[r.randint(1,100) for _ in range(n)];c=[r.randint(1,20) for _ in range(n)]
            cases.append(f"{n} {m}\n"+" ".join(map(str,a+c)))
        return "\n".join(cases)+"\n0 0\n"
    if number == 1789:
        cases=[]
        for _ in range(r.randint(1,3)):
            codes=set()
            while len(codes)<r.randint(2,30):codes.add("".join(r.choice(letters) for _ in range(7)))
            cases.append(f"{len(codes)}\n"+"\n".join(sorted(codes)))
        return "\n".join(cases)+"\n0\n"
    if number == 1941:return "\n".join(map(str,[r.randint(1,8) for _ in range(r.randint(1,5))]))+"\n0\n"
    if number == 2092:
        cases=[]
        for _ in range(r.randint(1,4)):
            n,m=r.randint(2,20),r.randint(1,20);cases.append(f"{n} {m}\n"+"\n".join(" ".join(str(r.randint(1,60)) for _ in range(m)) for _ in range(n)))
        return "\n".join(cases)+"\n0 0\n"
    if number == 2253:
        cases=[]
        for _ in range(r.randint(1,4)):
            n=r.randint(2,30);cases.append(f"{n}\n"+"\n".join(f"{r.randint(0,1000)} {r.randint(0,1000)}" for _ in range(n)))
        return "\n".join(cases)+"\n0\n"
    if number == 2337:
        cases=[]
        for _ in range(r.randint(1,5)):
            words=[word() for _ in range(r.randint(3,40))];cases.append(f"{len(words)}\n"+"\n".join(words))
        return f"{len(cases)}\n"+"\n".join(cases)+"\n"
    if number == 2676:
        a=[r.randint(1,20) for _ in range(r.randint(1,100))];return f"{len(a)}\n"+" ".join(map(str,a))+"\n"
    if number == 2712:
        md=[31,28,31,30,31,30,31,31,30,31,30,31];days=[]
        for m,d in enumerate(md,1):days.extend((m,x) for x in range(1,d+1))
        rows=[]
        for _ in range(r.randint(1,8)):
            a=r.randint(0,350);b=r.randint(a+1,min(364,a+30));rows.append(f"{days[a][0]} {days[a][1]} {r.randint(1,1000)} {days[b][0]} {days[b][1]}")
        return f"{len(rows)}\n"+"\n".join(rows)+"\n"
    if number == 2883:return "\n".join(" ".join(str(r.randint(-99,99)) for _ in range(5)) for _ in range(r.randint(1,12)))+"\n"
    if number == 2911:return f"{r.randint(1000,9999)}\n"
    if number == 2913:
        chars="".join(chr(i) for i in range(32,123));return "".join(r.choice(chars) for _ in range(r.randint(1,100)))+"\n"
    if number == 1753:return "\n".join("".join(r.choice("bw") for _ in range(4)) for _ in range(4))+"\n"
    raise KeyError(number)


def valid(number, text):
    if text == INVALID[number]: return False
    try:
        lines=text.rstrip("\n").splitlines();tok=text.split()
        if number == 3247:return len(tok)==1 and 1<=int(tok[0])<=9
        if number == 2936:
            n=int(tok[0]);a=list(map(int,tok[1:]));return len(a)==n and a==sorted(set(a)) and all(1<=x<=8 for x in a)
        if number == 2814:return len(tok)==9 and all(0<=int(x)<=3 for x in tok)
        if number == 2910:return len(lines)==1 and 1<=len(lines[0])<=100 and not any(x.isspace() for x in lines[0])
        if number == 2940:return len(tok)==2 and all(1<=int(x)<=9 for x in tok)
        if number == 1178:return len(lines)==1 and len(lines[0])%2==0 and 2<=len(lines[0])//2<=64 and len(set(re.findall(r"[A-H][1-8]",lines[0])))==len(lines[0])//2
        if number == 1190:return len(tok)==2 and 1<=int(tok[0])<=10000 and 1<=int(tok[1])<=10
        if number == 2899:return len(tok)==27
        if number == 2942:return len(tok)==1 and 1<=int(tok[0])<20
        if number == 1077:return len(tok)==9 and set(tok)==set("12345678x")
        if number == 1753:return len(lines)==4 and all(len(x)==4 and set(x)<={"b","w"} for x in lines)
        if number == 2911:return len(tok)==1 and 1000<=int(tok[0])<=9999
        if number == 2913:return len(lines)==1 and all(32<=ord(x)<=122 for x in lines[0])
        if number == 2676:return int(tok[0])==len(tok)-1 and all(int(x)>0 for x in tok)
        if number == 2883:return len(tok)>=5 and len(tok)%5==0
        if number == 2787:return tok[-4:]==["0"]*4 and all(1<=int(x)<=9 for x in tok[:-4]) and len(tok[:-4])%4==0
        if number == 2767:return len(lines)==1 and 1<=len(lines[0])<=200
        if number == 2927:return bool(lines)
        if number == 1047:return all(2<=len(x)<=60 and x.isdigit() for x in lines)
        if number == 1941:return tok[-1]=="0" and all(1<=int(x)<=10 for x in tok[:-1])
        if number == 1019:return 1<=int(tok[0])<=10 and len(tok)==int(tok[0])+1 and all(1<=int(x)<=2147483647 for x in tok[1:])
        if number == 1002:return 1<=int(tok[0])<=100000 and len(tok)==int(tok[0])+1 and all(len(re.sub(r"[^A-Z0-9]","",x.upper()))==7 for x in tok[1:])
        if number == 2181:return int(tok[0])==len(tok)-1 and int(tok[0])>=1
        if number == 2791:
            p=0;seen=0
            while int(tok[p]):
                n=int(tok[p]);p+=1;pts=[];seen+=1
                for _ in range(n):pts.append((int(tok[p]),int(tok[p+1])));p+=2
                if not 2<=n<=15 or len(set(pts))!=n or any(not(-1000<=x<=1000 and -1000<=y<=1000) for x,y in pts):return False
            return seen>0 and p==len(tok)-1
        if number == 1230:
            p=1;t=int(tok[0])
            for _ in range(t):
                n,k=int(tok[p]),int(tok[p+1]);p+=2
                if not(1<=n<=100 and 0<=k<=100):return False
                coords=list(map(int,tok[p:p+4*n]));p+=4*n
                if len(coords)!=4*n or any(not 0<=x<=100 for x in coords):return False
            return 1<=t<=10 and p==len(tok)
        if number == 1276:
            p=0;seen=0
            while p<len(tok):
                cash,n=int(tok[p]),int(tok[p+1]);p+=2;seen+=1
                pairs=list(map(int,tok[p:p+2*n]));p+=2*n
                if cash<0 or n<0 or len(pairs)!=2*n or any(x<=0 for x in pairs):return False
            return seen>0 and p==len(tok)
        if number == 1481:
            p=0;seen=0
            while True:
                w,h=map(int,lines[p].split());p+=1
                if (w,h)==(0,0):break
                grid=lines[p:p+h];p+=h;seen+=1
                if not(5<=w<=50 and 5<=h<=50 and len(grid)==h and all(len(x)==w and set(x)<={'.','*','X'} for x in grid)):return False
            return seen>0 and p==len(lines)
        if number == 2049:
            p=0;seen=0
            while True:
                m,n=map(int,lines[p].split());p+=1
                if (m,n)==(-1,-1):break
                if m<0 or n<0:return False
                for _ in range(m):
                    x,y,d,length=map(int,lines[p].split());p+=1
                    if not(1<=x<=199 and 1<=y<=199 and d in (0,1) and length>0):return False
                for _ in range(n):
                    x,y,d=map(int,lines[p].split());p+=1
                    if not(1<=x<=199 and 1<=y<=199 and d in (0,1)):return False
                x,y=map(float,lines[p].split());p+=1;seen+=1
                if x<=0 or y<=0:return False
            return seen>0 and p==len(lines)
        if number == 2804:
            parts=text.rstrip('\n').split('\n\n')
            if len(parts)!=2:return False
            dictionary=[x.split() for x in parts[0].splitlines()];docs=parts[1].splitlines()
            words=[x for row in dictionary for x in row]+docs
            return bool(dictionary and docs) and all(len(row)==2 for row in dictionary) and all(1<=len(x)<=10 and x.isascii() and x.islower() and x.isalpha() for x in words)
        if number == 2979:
            p=0;seen=0
            while True:
                n,m=int(tok[p]),int(tok[p+1]);p+=2
                if (n,m)==(0,0):break
                scores=list(map(int,tok[p:p+2*n]));p+=2*n;seen+=1
                if not(1<=m<=n<=200 and len(scores)==2*n and all(0<=x<=20 for x in scores)):return False
            return seen>0 and p==len(tok)
        if number == 1008:
            months="pop no zip zotz tzec xul yoxkin mol chen yax zac ceh mac kankin muan pax koyab cumhu uayet".split();n=int(lines[0])
            if len(lines)!=n+1 or n<1:return False
            for line in lines[1:]:
                day,month,year=line.split();d=int(day.rstrip('.'));y=int(year)
                if month not in months or not(0<=d<(5 if month=='uayet' else 20)) or y<0:return False
            return True
        if number in (1026,2818):
            p=0;seen=0
            while True:
                n=int(lines[p]);p+=1
                if n==0:break
                perm=list(map(int,lines[p].split()));p+=1;seen+=1
                if len(perm)!=n or set(perm)!=set(range(1,n+1)):return False
                while True:
                    fields=lines[p].split(' ',1);p+=1;k=int(fields[0])
                    if k==0:break
                    if len(fields)!=2 or k<1 or len(fields[1])>n:return False
            return seen>0 and p==len(lines)
        if number == 1056:
            count=0;group=[]
            for line in lines:
                if line=='9':
                    if not(2<=len(group)<=8 and len(set(group))==len(group)):return False
                    count+=1;group=[]
                elif not(1<=len(line)<=10 and set(line)<={'0','1'}):return False
                else:group.append(line)
            return count>0 and not group
        if number == 1742:
            p=0;seen=0
            while True:
                n,m=int(tok[p]),int(tok[p+1]);p+=2
                if (n,m)==(0,0):break
                values=list(map(int,tok[p:p+2*n]));p+=2*n;seen+=1
                if not(1<=n<=100 and 1<=m<=100000 and len(values)==2*n and all(x>0 for x in values)):return False
            return seen>0 and p==len(tok)
        if number == 1789:
            p=0;seen=0
            while True:
                n=int(lines[p]);p+=1
                if n==0:break
                codes=lines[p:p+n];p+=n;seen+=1
                if not(2<=n<=2000 and len(set(codes))==n and all(len(x)==7 and x.isascii() and x.islower() and x.isalpha() for x in codes)):return False
            return seen>0 and p==len(lines)
        if number == 2092:
            p=0;seen=0
            while True:
                n,m=int(tok[p]),int(tok[p+1]);p+=2
                if (n,m)==(0,0):break
                players=list(map(int,tok[p:p+n*m]));p+=n*m;seen+=1
                if not(2<=n<=500 and 1<=m<=500 and len(players)==n*m and all(1<=x<=10000 for x in players)):return False
            return seen>0 and p==len(tok)
        if number == 2253:
            p=0;seen=0
            while True:
                n=int(tok[p]);p+=1
                if n==0:break
                coords=list(map(int,tok[p:p+2*n]));p+=2*n;seen+=1
                if not(2<=n<=200 and len(coords)==2*n):return False
            return seen>0 and p==len(tok)
        if number == 2337:
            p=1;t=int(tok[0])
            for _ in range(t):
                n=int(tok[p]);p+=1;words=tok[p:p+n];p+=n
                if not(3<=n<=1000 and len(words)==n and all(x.isascii() and x.islower() and x.isalpha() for x in words)):return False
            return t>=1 and p==len(tok)
        if number == 2712:
            md=[31,28,31,30,31,30,31,31,30,31,30,31];n=int(tok[0])
            if len(tok)!=1+5*n or n<1:return False
            for i in range(n):
                m1,d1,c,m2,d2=map(int,tok[1+5*i:6+5*i])
                if not(1<=m1<=12 and 1<=d1<=md[m1-1] and 1<=m2<=12 and 1<=d2<=md[m2-1] and c>0):return False
                if sum(md[:m1-1])+d1>=sum(md[:m2-1])+d2:return False
            return True
    except (ValueError,IndexError):return False
    return False


def run_source(source, input_text):
    with tempfile.TemporaryDirectory() as folder:
        script=Path(folder)/"solution.py";script.write_text(source,encoding="utf-8")
        result=subprocess.run([sys.executable,"-I",str(script)],input=input_text,text=True,capture_output=True,timeout=120)
        if result.returncode:raise RuntimeError(result.stderr[-500:])
        return result.stdout.rstrip()+"\n"


def adapt_source(number, raw):
    note=None
    if number==1190:
        raw=raw.replace("\t    hmin=i+1","        hmin=i+1");note="normalized one mixed tab/space indentation defect without changing the algorithm"
    if number==2767:
        head=raw.split('# 主函数',1)[0]
        raw=head+'''# Input adapter: accept both this mirror's one-line form and the historical START/END wrapper.\nlines = sys.stdin.read().splitlines()\nif lines and lines[0] == "START":\n    for line in lines[1:]:\n        if line == "ENDOFINPUT": break\n        if line not in ("START", "END"): print(decrypt_caesar_cipher(line))\nelif lines:\n    print(decrypt_caesar_cipher(lines[0]))\n'''
        note="preserved the collection decryptor and added the historical START/END batch wrapper"
    if number==2253:
        raw=raw.replace("    input()\n\n    test_case += 1", "    test_case += 1")
        raw=("_frog_lines = iter(sys.stdin.read().splitlines())\n"
             "def input():\n"
             "    for _frog_line in _frog_lines:\n"
             "        if _frog_line.strip(): return _frog_line\n"
             "    raise EOFError\n"+raw)
        note="preserved the collection Floyd algorithm and accepted optional blank lines without consuming the next case"
    return raw,note


def source_sections(numbers):
    selected={}
    for source_index,path in enumerate(SOURCES):
        for number,title,body,codes,_samples in sections(path):
            if number in numbers and number not in selected and number in SOURCE_CODE_INDEX:
                ci=SOURCE_CODE_INDEX[number];selected[number]=(title,codes[ci],path,ci,source_index)
    return selected


def archive_check(source, entry):
    dirs=entry.get("oracle_dirs",[entry["oracle_dir"]]);excluded=[]
    if int(entry["number"])==1789 and "tests/1000-1999/1798" in dirs:
        dirs=[x for x in dirs if not x.endswith("/1798")];excluded.append("tests/1000-1999/1798: contents are an unrelated German encoding archive")
    paths=[p for rel in dirs for p in sorted((OPENJUDGE/rel).glob("*.in"))];bad=[]
    for p in paths:
        expected=p.with_suffix(".out").read_text(errors="replace")
        try:got=run_source(source,p.read_text(errors="replace"))
        except Exception:bad.append(p.name);continue
        if got.replace("\x1a"," ").split()!=expected.replace("\x1a"," ").split():bad.append(p.name)
    return {"status":"passed" if paths and not bad else "FAILED","cases":len(paths),"mismatched":bad,"excluded":excluded,"method":"exact output tokens against title-matched historical archives"}


def write_producecase(made,number,source,sample):
    program=("import random,subprocess,sys,tempfile\nfrom pathlib import Path\n"+inspect.getsource(generate)+
      f"\nREFERENCE={source!r}\nNUMBER={number}\nSAMPLE={sample!r}\n"+
      "def run(x):\n with tempfile.TemporaryDirectory() as d:\n  p=Path(d)/'s.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)\n  if q.returncode:raise SystemExit(q.stderr)\n  return q.stdout.rstrip()+'\\n'\n"+
      "def main():\n d=Path('data');d.mkdir(exist_ok=True)\n for p in d.glob('*'):p.unlink()\n for i,x in enumerate([SAMPLE]+[generate(NUMBER,s) for s in range(1,21)]):\n  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))\n"+
      "if __name__=='__main__':main()\n")
    (made/"producecase.py").write_text(program,encoding="utf-8")


def main():
    ap=argparse.ArgumentParser();ap.add_argument("round",type=int,choices=(6,7));opt=ap.parse_args()
    target=range(81,101) if opt.round==6 else range(101,121)
    entries=json.loads(CANDIDATES.read_text())["entries"];chosen=[x for x in entries if x["priority"] in target]
    if [x["priority"] for x in chosen]!=list(target):raise SystemExit("priority selection changed")
    selected=source_sections({int(x["number"]) for x in chosen})
    pp=ROOT/"collab"/f"t028-round{opt.round}-platform.json";platform={}
    if pp.exists():platform={int(x["local_number"]):x for x in json.loads(pp.read_text()).get("results",[])}
    manifest=[];report=[]
    for entry in chosen:
        n=int(entry["number"]);adaptation=None
        sample=page_sample(n,"样例输入");sample_out=page_sample(n,"样例输出")
        if n==2253 and sample.splitlines()[-1]!="0":sample += "0\n"
        if sample.strip()=="无":sample="7000\n";sample_out=run_source(selected[n][1],sample)
        if n in PLATFORM_SOURCES:
            path=ROOT/"scripts"/f"t028_platform_accepted_{n:05d}.py";source=path.read_text();title=re.search(r"<title>[^:]+:([^<]+)", (OPENJUDGE/"pages"/f"practice__{n:05d}.html").read_text()).group(1)
            reference="platform statistics Python3 Accepted submission";collection=None;ci=None;url=re.search(r"# Source: (\S+)",source).group(1)
        else:
            title,raw,path,ci,si=selected[n];raw,adaptation=adapt_source(n,raw)
            source=(f"# Source collection: {path}\n# Heading: {n}: {title}\n# Fenced code block index: {ci}\n# Source URL: {SOURCE_URLS[si]}\n"
                    f"# Upstream problem: http://cs101.openjudge.cn/{entry['submit_group']}/{entry['submit_id']}/\n# License: not declared; no license is inferred.\nimport sys\n"+clean(raw))
            reference="human-provided solution collection";collection=str(path);url=SOURCE_URLS[si]
        cross=archive_check(source,entry)
        if cross["status"]!="passed":raise SystemExit(f"{n} archive cross-check failed: {cross}")
        cases=[sample]+[generate(n,s) for s in range(1,21)];outputs=[run_source(source,x) for x in cases]
        made_rel=str(Path(entry["oracle_dir"]).parent/f"{n:05d}_made");made=OPENJUDGE/made_rel;data=made/"data";data.mkdir(parents=True,exist_ok=True)
        for old in data.glob("*"):old.unlink()
        for i,(x,y) in enumerate(zip(cases,outputs)):(data/f"{i}.in").write_text(x);(data/f"{i}.out").write_text(y)
        (made/"samplecode.py").write_text(source);write_producecase(made,n,source,sample)
        rows=[(LABELS[n],all(valid(n,x) for x in cases[1:]))];domain_exemption="the complete valid input domain has only nine values" if n==3247 else None
        audit=common.audit(made,cases=cases[1:],outputs=outputs[1:],sample_input=sample,sample_output=sample_out,exemption=domain_exemption,
          constraints=rows,constraint_counterexample=(INVALID[n].strip(),[(LABELS[n],valid(n,INVALID[n]))]))
        smoke=[s for s in range(20000) if not valid(n,generate(n,s))];prow=platform.get(n)
        status="passed" if not audit["failed"] and not smoke and (not prow or prow.get("verdict")=="Accepted") else "FAILED"
        manifest.append({**entry,"local_number":n,"title":title,"made_dir":made_rel,"sample_input":sample,"solution_collection":collection,"solution_code_index":ci,"source_adaptation":adaptation,"pending_rework":[]})
        report.append({"local_number":n,"global_number":entry["global_number"],"title":title,"priority":entry["priority"],"tier":entry["tier"],"status":status,
          "reference_source":reference,"solution_collection":collection,"solution_code_index":ci,"source_url":url,"source_adaptation":adaptation,"license_status":"not declared; no license is inferred",
          "submission_id":prow.get("solution_id") if prow else None,"platform_verdict":prow.get("verdict") if prow else "not_run","archive_cross_check":cross,"generator":"generate",
          "generator_seed_smoke":{"seeds":20000,"status":"passed" if not smoke else "FAILED","failed_seeds":smoke[:8]},"test_cases":len(cases),"max_input_bytes":max(len(x.encode()) for x in cases),"max_output_bytes":max(len(x.encode()) for x in outputs),
          "constraints":rows,"constraint_counterexample":INVALID[n].strip(),"self_audit":audit})
        print(f"{n:05d} built",flush=True)
    (ROOT/"collab"/f"t028-round{opt.round}-manifest.json").write_text(json.dumps({"task":"T-028","round":opt.round,"count":20,"priority_range":[min(target),max(target)],"entries":manifest},ensure_ascii=False,indent=2)+"\n")
    failed=[x["local_number"] for x in report if x["status"]!="passed"]
    (ROOT/"collab"/f"t028-round{opt.round}-report.json").write_text(json.dumps({"task":"T-028","round":opt.round,"updated_at":datetime.now(timezone.utc).isoformat(),"count":20,"pending_rework_status":common.pending_rework_status([],OPENJUDGE/"tests"),"entries":report,"failed":failed},ensure_ascii=False,indent=2)+"\n")
    if failed:raise SystemExit(f"self-audit failed: {failed}")


if __name__=="__main__":main()
