# External reference: /practice/29742/statistics/
# Accepted submission: 52733624
# Source: http://cs101.openjudge.cn/practice/solution/52733624/
# License: not declared on the submission page; no license is inferred.

def calc(sentence):
    # 1. 分割成音节列表
    s = sentence.replace(' ', '')
    arr = []
    for i in range(0, len(s), 2):
        arr.append(s[i:i+2])
    
    # 2. 统计 PO -> PI -> PA 数量
    po = 0   # PO 总数
    pip = 0  # PO+PI 对数
    res = 0  # 最终答案
    
    for word in arr:
        if word == 'PA':
            res += pip
        elif word == 'PI':
            pip += po
        elif word == 'PO':
            po += 1
    return res

# 循环读入直到结束
while True:
    try:
        line = input()
        print(calc(line))
    except:
        break