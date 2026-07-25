# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# 定义加权因子字符串（通过字母编码，避免显式列表）
# 对应的权重为：[7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1]
# 原理：ord('h') - ord('a') = 104 - 97 = 7，以此类推
WEIGHT_CODE = 'hjkfiecbgdhjkfiecb'

# 模11后对应的校验码余数表（用于验证总和模11是否应为1）
# 这是一个数学性质：合法身份证的加权总和 % 11 == 1
# 详细推导见下方说明

def verify_id_card(id_number):
    """
    验证一个18位中国居民身份证号码是否合法（仅校验位验证）
    
    参数:
        id_number (str): 18位身份证号码，最后一位可以是'X'或'x'
    
    返回:
        bool: 合法返回 True，否则返回 False
    """
    # 步骤1：检查长度是否为18位
    if len(id_number) != 18:
        return False

    # 步骤2：将输入中的 'X' 或 'x' 替换为 ':'，以便 ord(':') - 48 = 10
    # 这是一个巧妙的ASCII技巧，避免额外判断
    cleaned_id = id_number.replace('X', ':').replace('x', ':')

    # 步骤3：检查前17位是否全为数字，第18位是否为数字或':'
    if not cleaned_id[:17].isdigit() or not (cleaned_id[17].isdigit() or cleaned_id[17] == ':'):
        return False

    # 步骤4：计算加权和
    total_weighted_sum = 0
    for i in range(18):
        # 获取第i位的权重（通过字符编码转换）
        weight = ord(WEIGHT_CODE[i]) - ord('a')
        # 获取第i位的数值（字符转数字，':' 表示10）
        digit_value = ord(cleaned_id[i]) - 48  # ord('0') = 48
        total_weighted_sum += weight * digit_value
        # 每步取模防止整数溢出（可选，但安全）
        total_weighted_sum %= 11

    # 步骤5：根据数学性质，合法身份证的加权和模11必须等于1
    return total_weighted_sum == 1


def main():
    """主函数：读取多个身份证号码并验证"""
    try:
        n = int(input().strip())  # 输入测试用例数量
        for _ in range(n):
            identity = input().strip()  # 读取身份证号码
            if verify_id_card(identity):
                print('YES')
            else:
                print('NO')
    except Exception as e:
        # 防止输入异常导致程序崩溃
        print("NO")


# 运行程序
if __name__ == '__main__':
    main()
