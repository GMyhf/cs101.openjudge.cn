# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def power_of_two_representation(n):
    # 函数用于找到小于或等于n的最大2的幂次
    def find_max_power(n):
        power = 0
        while (1 << power) <= n:
            power += 1
        return power - 1

    # 函数用于将幂次表示为2的幂次方的表示
    def represent_power(power):
        if power == 1:
            return '2'
        elif power == 0:
            return '2(0)'
        else:
            return '2(' + power_of_two_representation(power) + ')'

    # 特殊情况：如果n是0，直接返回空字符串
    if n == 0:
        return ''

    result = ''
    while n > 0:
        max_power = find_max_power(n)
        # 如果结果字符串不为空，添加加号
        if result:
            result += '+'
        # 把最大幂次转换为2的幂次方的表示
        result += represent_power(max_power)
        # 减去已经表示的数，继续寻找余数的表示
        n -= 1 << max_power

    return result

print(power_of_two_representation(int(input())))
