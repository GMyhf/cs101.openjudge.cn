"""31381自产参考：将整行字符反转，来源为本仓库实现，无外部提交代码。"""
import sys


def solve(text):
    if text.endswith('\n'):
        text = text[:-1]
        if text.endswith('\r'):
            text = text[:-1]
    return text[::-1]


if __name__ == '__main__':
    print(solve(sys.stdin.read()))
