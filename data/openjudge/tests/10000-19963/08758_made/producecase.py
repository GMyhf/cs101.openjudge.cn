import random, subprocess, tempfile
from pathlib import Path
SAMPLE_IN = '137\n'
SAMPLE_OUT = '2(2(2)+2+2(0))+2(2+2(0))+2(0)\n'
CASES = ['137\n', '6894\n', '5782\n', '10003\n', '8884\n', '309\n', '6950\n', '9683\n', '7877\n', '4698\n', '12644\n', '16838\n', '7837\n', '17923\n', '8078\n', '3027\n', '4180\n', '15770\n', '2471\n', '7609\n']
REFERENCE_SOURCE = "def power_of_two_representation(n):\n    # 函数用于找到小于或等于n的最大2的幂次\n    def find_max_power(n):\n        power = 0\n        while (1 << power) <= n:\n            power += 1\n        return power - 1\n\n    # 函数用于将幂次表示为2的幂次方的表示\n    def represent_power(power):\n        if power == 1:\n            return '2'\n        elif power == 0:\n            return '2(0)'\n        else:\n            return '2(' + power_of_two_representation(power) + ')'\n\n    # 特殊情况：如果n是0，直接返回空字符串\n    if n == 0:\n        return ''\n\n    result = ''\n    while n > 0:\n        max_power = find_max_power(n)\n        # 如果结果字符串不为空，添加加号\n        if result:\n            result += '+'\n        # 把最大幂次转换为2的幂次方的表示\n        result += represent_power(max_power)\n        # 减去已经表示的数，继续寻找余数的表示\n        n -= 1 << max_power\n\n    return result\n\nprint(power_of_two_representation(int(input())))\n"
assert CASES[0] == SAMPLE_IN
random.seed(8758)
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
root = Path(__file__).parent / "data"
for index, content in enumerate(CASES):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")
