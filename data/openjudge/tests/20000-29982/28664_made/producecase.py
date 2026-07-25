import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '# 定义加权因子字符串（通过字母编码，避免显式列表）\n# 对应的权重为：[7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1]\n# 原理：ord(\'h\') - ord(\'a\') = 104 - 97 = 7，以此类推\nWEIGHT_CODE = \'hjkfiecbgdhjkfiecb\'\n\n# 模11后对应的校验码余数表（用于验证总和模11是否应为1）\n# 这是一个数学性质：合法身份证的加权总和 % 11 == 1\n# 详细推导见下方说明\n\ndef verify_id_card(id_number):\n    """\n    验证一个18位中国居民身份证号码是否合法（仅校验位验证）\n    \n    参数:\n        id_number (str): 18位身份证号码，最后一位可以是\'X\'或\'x\'\n    \n    返回:\n        bool: 合法返回 True，否则返回 False\n    """\n    # 步骤1：检查长度是否为18位\n    if len(id_number) != 18:\n        return False\n\n    # 步骤2：将输入中的 \'X\' 或 \'x\' 替换为 \':\'，以便 ord(\':\') - 48 = 10\n    # 这是一个巧妙的ASCII技巧，避免额外判断\n    cleaned_id = id_number.replace(\'X\', \':\').replace(\'x\', \':\')\n\n    # 步骤3：检查前17位是否全为数字，第18位是否为数字或\':\'\n    if not cleaned_id[:17].isdigit() or not (cleaned_id[17].isdigit() or cleaned_id[17] == \':\'):\n        return False\n\n    # 步骤4：计算加权和\n    total_weighted_sum = 0\n    for i in range(18):\n        # 获取第i位的权重（通过字符编码转换）\n        weight = ord(WEIGHT_CODE[i]) - ord(\'a\')\n        # 获取第i位的数值（字符转数字，\':\' 表示10）\n        digit_value = ord(cleaned_id[i]) - 48  # ord(\'0\') = 48\n        total_weighted_sum += weight * digit_value\n        # 每步取模防止整数溢出（可选，但安全）\n        total_weighted_sum %= 11\n\n    # 步骤5：根据数学性质，合法身份证的加权和模11必须等于1\n    return total_weighted_sum == 1\n\n\ndef main():\n    """主函数：读取多个身份证号码并验证"""\n    try:\n        n = int(input().strip())  # 输入测试用例数量\n        for _ in range(n):\n            identity = input().strip()  # 读取身份证号码\n            if verify_id_card(identity):\n                print(\'YES\')\n            else:\n                print(\'NO\')\n    except Exception as e:\n        # 防止输入异常导致程序崩溃\n        print("NO")\n\n\n# 运行程序\nif __name__ == \'__main__\':\n    main()\n'
SAMPLE_IN = '2\n371311200312247819\n130631197601191234\n'
SAMPLE_OUT = 'YES\nNO\n'
def generate_case(r):
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]; mapping = "10X98765432"
    ids = []
    for _ in range(r.randint(2, 8)):
        prefix = "".join(str(r.randint(0, 9)) for _ in range(17)); check = mapping[sum(int(a) * b for a, b in zip(prefix, weights)) % 11]
        if r.random() < .35: check = "0" if check != "0" else "1"
        ids.append(prefix + check)
    return str(len(ids)) + "\n" + "\n".join(ids) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(28664 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
