import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/23742/\n# Accepted submission: 43299870\n# Source: http://cs101.openjudge.cn/practice/solution/43299870/\n# License: not declared on the submission page; no license is inferred.\n\ndef is_palindrome(date):\n    date_str = str(date)\n    return date_str == date_str[::-1]\n\ndef generate_palindrome_dates(start_date, end_date):\n    palindrome_dates = []\n    for year in range(1000, 10000):\n        for month in {1,3,5,7,8,10,12}:\n            for day in range(1, 32):\n                date = year * 10000 + month * 100 + day\n                if start_date <= date <= end_date and is_palindrome(date):\n                    palindrome_dates.append(str(date))\n        for month in {4,6,9,11}:\n            for day in range(1, 31):\n                date = year * 10000 + month * 100 + day\n                if start_date <= date <= end_date and is_palindrome(date):\n                    palindrome_dates.append(str(date))\n        for month in {2}:\n            for day in range(1, 30):\n                date = year * 10000 + month * 100 + day\n                if start_date <= date <= end_date and is_palindrome(date):\n                    palindrome_dates.append(str(date))\n    return palindrome_dates\n\nstart_date = 10000101\nend_date=int(input())\npalindrome_dates = generate_palindrome_dates(start_date, end_date)\n\nprint(" ".join(palindrome_dates))\n'
SAMPLE='11001231\n'
GENERATOR_NAME='g23742'
def g23742(r): return f"{r.randint(10000101,50001231)}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
