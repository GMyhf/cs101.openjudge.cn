import random, re, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/23742/\n# Accepted submission: 43299870\n# Source: http://cs101.openjudge.cn/practice/solution/43299870/\n# License: not declared on the submission page; no license is inferred.\n\ndef is_palindrome(date):\n    date_str = str(date)\n    return date_str == date_str[::-1]\n\ndef generate_palindrome_dates(start_date, end_date):\n    palindrome_dates = []\n    for year in range(1000, 10000):\n        for month in {1,3,5,7,8,10,12}:\n            for day in range(1, 32):\n                date = year * 10000 + month * 100 + day\n                if start_date <= date <= end_date and is_palindrome(date):\n                    palindrome_dates.append(str(date))\n        for month in {4,6,9,11}:\n            for day in range(1, 31):\n                date = year * 10000 + month * 100 + day\n                if start_date <= date <= end_date and is_palindrome(date):\n                    palindrome_dates.append(str(date))\n        for month in {2}:\n            for day in range(1, 30):\n                date = year * 10000 + month * 100 + day\n                if start_date <= date <= end_date and is_palindrome(date):\n                    palindrome_dates.append(str(date))\n    return palindrome_dates\n\nstart_date = 10000101\nend_date=int(input())\npalindrome_dates = generate_palindrome_dates(start_date, end_date)\n\nprint(" ".join(palindrome_dates))\n'
SAMPLE='11001231\n'
GENERATOR_NAME='g23742'
def g23742(r): return f"{r.randint(10000101,50001231)}\n"

def _is_date(v):
    y,m,d=v//10000,v//100%100,v%100
    if not 1<=m<=12: return False
    leap = y%4==0 and (y%100!=0 or y%400==0)
    md=[31,29 if leap else 28,31,30,31,30,31,31,30,31,30,31][m-1]
    return 1<=d<=md

def valid(text):
    """题面：一行，一个合法日期 xxxxyyzz，10000101 <= xxxxyyzz <= 50001231。"""
    lines=text.split('\n')
    if lines and lines[-1]=='': lines.pop()
    if len(lines)!=1: return False
    t=lines[0].split()
    if len(t)!=1 or not re.fullmatch(r'[1-9][0-9]{7}',t[0]): return False
    v=int(t[0])
    return 10000101<=v<=50001231 and _is_date(v)

def _rand_date(r,y0,y1):
    while True:
        y=r.randint(y0,y1); m=r.randint(1,12); d=r.randint(1,31)
        v=y*10000+m*100+d
        if _is_date(v) and 10011001<=v<=50001231: return v

def build_cases():
    # 只用合法日期作输入；不出比第一个回文日期 10011001 更早的日期（那时输出为空，题面没规定空输出的形式）
    fixed=[
        10011001,   # 恰好等于第一个回文日期（闭区间）
        10011002, 10100101, 10100100+31,
        13100131,   # 恰好是 1 月 31 日回文
        13111130,   # 13111131（11 月 31 日）不合法，不能输出
        13111201, 13300331, 13400430, 13400501,  # 13400431 四月无 31 日
        13600701, 13900930, 13901001,            # 13600631、13900931 不合法
        11200211, 11200212, 12100121,
        20211202, 20200202, 22000222, 29991231,
        42900923, 42900924,  # 最后一个回文日期 42900924 前后
        49991231, 50000101, 50001231,  # 上界
    ]
    rand=[]
    for k,(y0,y1) in enumerate([(1001,1400)]*5+[(1400,5000)]*9):
        rand.append(_rand_date(random.Random(23742*100+k),y0,y1))
    vals=fixed+rand
    assert len(vals)==len(set(vals))==39
    return [SAMPLE]+[f"{v}\n" for v in vals]

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=build_cases()
    assert len(cases)==40 and all(valid(c) for c in cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
