# External reference: /practice/30061/statistics/
# Accepted submission: 52831600
# Source: http://cs101.openjudge.cn/practice/solution/52831600/
# License: not declared on the submission page; no license is inferred.

import sys

def main():
    # 读取所有输入数据
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    # 解析 N 和 M
    N = int(input_data[0])
    M = int(input_data[1])
    
    # 将报出的编号放入集合中，便于快速查找
    reported_students = set(map(int, input_data[2:2+M]))
    
    # 找出未到达的同学编号
    missing_students = []
    for i in range(N):
        if i not in reported_students:
            missing_students.append(i)
            
    # 根据要求输出结果
    if not missing_students:
        print(N)
    else:
        print(*(missing_students))

if __name__ == '__main__':
    main()