# External reference: statistics page /practice/28908/
# Accepted submission: 52734356
# Source: http://cs101.openjudge.cn/practice/solution/52734356/
# License: not declared on the submission page; no license is inferred.

# 初始化变量
a = b = c = 0
s = input().strip()

# 按分号分割语句
statements = s.split(';')
for stmt in statements:
    stmt = stmt.strip()
    if not stmt:
        continue
    # 提取变量和值
    var = stmt[0]       # 第一个字符是变量名
    num = stmt[-1]     # 最后一个字符是数字
    # 赋值
    if var == 'a':
        a = int(num)
    elif var == 'b':
        b = int(num)
    elif var == 'c':
        c = int(num)

# 输出结果
print(a, b, c)