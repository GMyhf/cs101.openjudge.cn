import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '# 定义加权因子字符串（通过字母编码，避免显式列表）\n# 对应的权重为：[7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1]\n# 原理：ord(\'h\') - ord(\'a\') = 104 - 97 = 7，以此类推\nWEIGHT_CODE = \'hjkfiecbgdhjkfiecb\'\n\n# 模11后对应的校验码余数表（用于验证总和模11是否应为1）\n# 这是一个数学性质：合法身份证的加权总和 % 11 == 1\n# 详细推导见下方说明\n\ndef verify_id_card(id_number):\n    """\n    验证一个18位中国居民身份证号码是否合法（仅校验位验证）\n    \n    参数:\n        id_number (str): 18位身份证号码，最后一位可以是\'X\'或\'x\'\n    \n    返回:\n        bool: 合法返回 True，否则返回 False\n    """\n    # 步骤1：检查长度是否为18位\n    if len(id_number) != 18:\n        return False\n\n    # 步骤2：将输入中的 \'X\' 或 \'x\' 替换为 \':\'，以便 ord(\':\') - 48 = 10\n    # 这是一个巧妙的ASCII技巧，避免额外判断\n    cleaned_id = id_number.replace(\'X\', \':\').replace(\'x\', \':\')\n\n    # 步骤3：检查前17位是否全为数字，第18位是否为数字或\':\'\n    if not cleaned_id[:17].isdigit() or not (cleaned_id[17].isdigit() or cleaned_id[17] == \':\'):\n        return False\n\n    # 步骤4：计算加权和\n    total_weighted_sum = 0\n    for i in range(18):\n        # 获取第i位的权重（通过字符编码转换）\n        weight = ord(WEIGHT_CODE[i]) - ord(\'a\')\n        # 获取第i位的数值（字符转数字，\':\' 表示10）\n        digit_value = ord(cleaned_id[i]) - 48  # ord(\'0\') = 48\n        total_weighted_sum += weight * digit_value\n        # 每步取模防止整数溢出（可选，但安全）\n        total_weighted_sum %= 11\n\n    # 步骤5：根据数学性质，合法身份证的加权和模11必须等于1\n    return total_weighted_sum == 1\n\n\ndef main():\n    """主函数：读取多个身份证号码并验证"""\n    try:\n        n = int(input().strip())  # 输入测试用例数量\n        for _ in range(n):\n            identity = input().strip()  # 读取身份证号码\n            if verify_id_card(identity):\n                print(\'YES\')\n            else:\n                print(\'NO\')\n    except Exception as e:\n        # 防止输入异常导致程序崩溃\n        print("NO")\n\n\n# 运行程序\nif __name__ == \'__main__\':\n    main()\n'
SAMPLE_IN = '2\n371311200312247819\n130631197601191234\n'
SAMPLE_OUT = 'YES\nNO\n'
import datetime

WEIGHTS = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
MAPPING = "10X98765432"

def valid(text):
    """题面：第一行正整数 n (1<=n<=50)；接下来 n 行各一个身份证号：18 位，
    前 17 位为数字且保证合法（这里只能核出生日期第 7-14 位是真实日期），最后一位为数字或大写 X。"""
    if not isinstance(text, str) or not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit() or lines[0][0] == "0" or not 1 <= int(lines[0]) <= 50:
        return False
    n = int(lines[0])
    if len(lines) != n + 1:
        return False
    for s in lines[1:]:
        if len(s) != 18 or not s[:17].isdigit() or not (s[17].isdigit() or s[17] == "X"):
            return False
        try:
            datetime.date(int(s[6:10]), int(s[10:12]), int(s[12:14]))
        except ValueError:
            return False
    return True

def make_id(r, good, want_x=False):
    while True:
        region = str(r.randint(110000, 659999))
        day = datetime.date(1930, 1, 1) + datetime.timedelta(days=r.randint(0, 34000))
        prefix = region + day.strftime("%Y%m%d") + "%03d" % r.randint(0, 999)
        check = MAPPING[sum(int(a) * b for a, b in zip(prefix, WEIGHTS)) % 11]
        if want_x and check != "X":
            continue
        break
    if not good:
        if r.random() < .3 and check != "X":
            check = "X"
        else:
            check = r.choice([c for c in "0123456789X" if c != check])
    return prefix + check

def generate_case(r, index):
    if index in (1, 2):
        n = 1
    elif index % 4 == 0 or index >= 17:
        n = 50
    else:
        n = r.randint(2, 50)
    if index == 3:
        flags = [True] * n            # 全 YES
    elif index == 4:
        flags = [False] * n           # 全 NO
    else:
        flags = [r.random() < .5 for _ in range(n)]
    if index == 1:
        flags = [True]
    if index == 2:
        flags = [False]
    ids = [make_id(r, g, want_x=(g and r.random() < .2) or index == 1) for g in flags]
    return str(n) + "\n" + "\n".join(ids) + "\n"

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(20):
            if index == 0: content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(28664 + index + attempt * 1000), index)
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content), index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()
