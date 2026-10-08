import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def threeSum(nums):\n    nums.sort()  # 先对数组排序\n    result = []\n    n = len(nums)\n\n    for i in range(n - 2):\n        # 跳过重复的元素\n        if i > 0 and nums[i] == nums[i - 1]:\n            continue\n\n        # 双指针\n        left = i + 1\n        right = n - 1\n\n        while left < right:\n            total = nums[i] + nums[left] + nums[right]\n\n            if total < 0:\n                left += 1\n            elif total > 0:\n                right -= 1\n            else:\n                result.append([nums[i], nums[left], nums[right]])\n\n                # 跳过重复的元素\n                while left < right and nums[left] == nums[left + 1]:\n                    left += 1\n                while left < right and nums[right] == nums[right - 1]:\n                    right -= 1\n\n                left += 1\n                right -= 1\n\n    return len(result)\n\n*nums, = map(int, input().split())\n#nums = [-1, 0, 1, 2, -1, -4]\ncount = threeSum(nums)\nprint(count)  \n'
SAMPLE_IN = '-1 0 1 2 -1 -4\n'
SAMPLE_OUT = '2\n'
def generate_case(r):
    values = [r.randint(-100, 100) for _ in range(r.randint(6, 45))]
    assert len(values) <= 3000
    return " ".join(map(str, values)) + "\n"

def valid(text):
    """题面：一行 n 个整数，n<=3000（题面没给数值范围，只核整数格式与个数，另要求 n>=1）。"""
    import re
    lines=text.split('\n')
    if lines and lines[-1]=='': lines.pop()
    if len(lines)!=1: return False
    t=lines[0].split()
    return 1<=len(t)<=3000 and all(re.fullmatch(r'-?[0-9]+',v) for v in t)

def big_case(r,n,lo,hi,kind='rand'):
    if kind=='zeros': values=[0]*n
    elif kind=='pos': values=[r.randint(1,hi) for _ in range(n)]
    elif kind=='mixzero': values=[r.choice([0,0,0,r.randint(lo,hi)]) for _ in range(n)]
    else: values=[r.randint(lo,hi) for _ in range(n)]
    return " ".join(map(str,values))+"\n"

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        # 第 10..19 组：边界与满规模 n=3000（卡掉 O(n^3) 暴力）
        special = [(1,0,0,'rand'),(2,-5,5,'rand'),(3,0,0,'zeros'),(3000,0,0,'zeros'),(3000,1,10**6,'pos'),
                   (3000,-50,50,'rand'),(3000,-1000,1000,'rand'),(3000,-10**5,10**5,'rand'),
                   (3000,-10**8,10**8,'rand'),(3000,-300,300,'mixzero')]
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            elif index >= 10:
                n, lo, hi, kind = special[index - 10]
                content = big_case(random.Random(23806 * 100 + index), n, lo, hi, kind)
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(23806 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content) and content not in seen[1:]
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
