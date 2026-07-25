import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def threeSum(nums):\n    nums.sort()  # 先对数组排序\n    result = []\n    n = len(nums)\n\n    for i in range(n - 2):\n        # 跳过重复的元素\n        if i > 0 and nums[i] == nums[i - 1]:\n            continue\n\n        # 双指针\n        left = i + 1\n        right = n - 1\n\n        while left < right:\n            total = nums[i] + nums[left] + nums[right]\n\n            if total < 0:\n                left += 1\n            elif total > 0:\n                right -= 1\n            else:\n                result.append([nums[i], nums[left], nums[right]])\n\n                # 跳过重复的元素\n                while left < right and nums[left] == nums[left + 1]:\n                    left += 1\n                while left < right and nums[right] == nums[right - 1]:\n                    right -= 1\n\n                left += 1\n                right -= 1\n\n    return len(result)\n\n*nums, = map(int, input().split())\n#nums = [-1, 0, 1, 2, -1, -4]\ncount = threeSum(nums)\nprint(count)  \n'
SAMPLE_IN = '-1 0 1 2 -1 -4\n'
SAMPLE_OUT = '2\n'
def generate_case(r):
    values = [r.randint(-100, 100) for _ in range(r.randint(6, 45))]
    assert len(values) <= 3000
    return " ".join(map(str, values)) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(23806 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
