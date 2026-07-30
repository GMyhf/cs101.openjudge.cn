# External reference: http://cs101.openjudge.cn/practice/29335/statistics/
# Accepted submission: 52829517
# Source: http://cs101.openjudge.cn/practice/solution/52829517/
# License: not declared on the submission page; no license is inferred.

import sys

def simplify_path(path: str) -> str:
    # 将路径按照 '/' 分割
    parts = path.split('/')
    stack = []

    for part in parts:
        if part == '' or part == '.':
            # 忽略空部分或当前目录
            continue
        elif part == '..':
            # 返回上一级，如果栈不为空则弹出
            if stack:
                stack.pop()
        else:
            # 合法的目录/文件名入栈
            stack.append(part)

    # 拼接并返回规范路径
    return '/' + '/'.join(stack)

def main():
    # 循环读取标准输入，直到文件末尾（EOF）
    for line in sys.stdin:
        path = line.strip()
        if path:
            print(simplify_path(path))

if __name__ == '__main__':
    main()
