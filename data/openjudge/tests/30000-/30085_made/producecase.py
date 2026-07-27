import random
REFERENCE="# External reference: /practice/30085/statistics/\n# Accepted submission: 52831605\n# Source: http://cs101.openjudge.cn/practice/solution/52831605/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef main():\n    # 读取所有输入数据\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    w = int(input_data[0])\n    n = int(input_data[1])\n    prices = [int(x) for x in input_data[2:2+n]]\n    \n    # 升序排序\n    prices.sort()\n    \n    left = 0\n    right = n - 1\n    group_count = 0\n    \n    # 双指针扫描\n    while left <= right:\n        if left == right:\n            # 只剩下一个纪念品，单独一组\n            group_count += 1\n            break\n        \n        if prices[left] + prices[right] <= w:\n            # 两个可以分在同一组\n            left += 1\n            right -= 1\n        else:\n            # 最贵的纪念品只能单独一组\n            right -= 1\n        \n        group_count += 1\n        \n    print(group_count)\n\nif __name__ == '__main__':\n    main()"
SAMPLE='100 \n9 \n90 \n20 \n20 \n30 \n50 \n60 \n70 \n80 \n90\n'
GENERATOR_NAME='g30085'
def g30085(r):
    n = r.randint(1, 200); w = r.randint(1, 2000); prices = [r.randint(1, w) for _ in range(n)]
    return f"{w}\n{n}\n" + "\n".join(map(str, prices)) + "\n"

from pathlib import Path
import random, subprocess, sys, tempfile
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()
