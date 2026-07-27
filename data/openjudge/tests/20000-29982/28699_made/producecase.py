import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/28699/\n# Accepted submission: 52832114\n# Source: http://cs101.openjudge.cn/practice/solution/52832114/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\nfrom collections import Counter\n\ndef solve():\n    # 读取所有输入\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    n = int(input_data[0])\n    m = int(input_data[1])\n    \n    # 提取价格并从小到大排序\n    prices = [int(x) for x in input_data[2:2+n]]\n    prices.sort()\n    \n    # 提取水果清单\n    fruits = input_data[2+n : 2+n+m]\n    \n    # 统计每种水果的出现频次，并按频次从大到小排序\n    counter = Counter(fruits)\n    frequencies = list(counter.values())\n    frequencies.sort(reverse=True)\n    \n    # 计算最小总价：高频次配低价格\n    min_price = sum(freq * price for freq, price in zip(frequencies, prices))\n    \n    # 计算最大总价：高频次配高价格\n    max_price = sum(freq * price for freq, price in zip(frequencies, prices[::-1]))\n    \n    print(min_price, max_price)\n\nif __name__ == '__main__':\n    solve()"
SAMPLE='5 3\n4 2 1 10 5\napple\norange\nmango\n'
EXTRA_CASE='100 100\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100\nfruit0\nfruit1\nfruit2\nfruit3\nfruit4\nfruit5\nfruit6\nfruit7\nfruit8\nfruit9\nfruit10\nfruit11\nfruit12\nfruit13\nfruit14\nfruit15\nfruit16\nfruit17\nfruit18\nfruit19\nfruit20\nfruit21\nfruit22\nfruit23\nfruit24\nfruit25\nfruit26\nfruit27\nfruit28\nfruit29\nfruit30\nfruit31\nfruit32\nfruit33\nfruit34\nfruit35\nfruit36\nfruit37\nfruit38\nfruit39\nfruit40\nfruit41\nfruit42\nfruit43\nfruit44\nfruit45\nfruit46\nfruit47\nfruit48\nfruit49\nfruit50\nfruit51\nfruit52\nfruit53\nfruit54\nfruit55\nfruit56\nfruit57\nfruit58\nfruit59\nfruit60\nfruit61\nfruit62\nfruit63\nfruit64\nfruit65\nfruit66\nfruit67\nfruit68\nfruit69\nfruit70\nfruit71\nfruit72\nfruit73\nfruit74\nfruit75\nfruit76\nfruit77\nfruit78\nfruit79\nfruit80\nfruit81\nfruit82\nfruit83\nfruit84\nfruit85\nfruit86\nfruit87\nfruit88\nfruit89\nfruit90\nfruit91\nfruit92\nfruit93\nfruit94\nfruit95\nfruit96\nfruit97\nfruit98\nfruit99\n'
GENERATOR_NAME='g28699'
def g28699(r):
    n, m = r.randint(1, 30), r.randint(1, 30); prices = [r.randint(1, 100) for _ in range(n)]
    names = [f"fruit{i}" for i in range(n)]; chosen = names[:r.randint(1, n)]
    return f"{n} {m}\n{' '.join(map(str, prices))}\n" + "\n".join(r.choice(chosen) for _ in range(m)) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+([EXTRA_CASE] if EXTRA_CASE else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()
