# External reference: http://cs101.openjudge.cn/practice/30162/statistics/
# Accepted submission: 52723723
# Source: http://cs101.openjudge.cn/practice/solution/52723723/
# License: not declared on the submission page; no license is inferred.

from math import sin, cos, tan
import sys

def main():
    input = sys.stdin.read().splitlines()
    ptr = 0
    t = int(input[ptr].strip())
    ptr += 1

    for _ in range(t):
        # 1. 解析常量定义
        line = input[ptr].strip()
        ptr += 1
        parts = line.split()
        m = int(parts[0])
        const = {}
        try:
            for i in range(m):
                name = parts[1 + 2*i]
                val = float(parts[2 + 2*i])
                const[name] = val
        except:
            # 常量定义非法（题目保证输入合法，防御性处理）
            pass

        # 2. 构建安全的计算环境：仅允许指定函数 + 自定义常量
        safe_env = {
            "sin": sin,
            "cos": cos,
            "tan": tan,
            "abs": abs
        }
        safe_env.update(const)  # 加入自定义常量

        # 3. 读取并清理表达式
        expr = input[ptr].strip()
        ptr += 1
        expr = expr.replace(" ", "")  # 移除所有空格

        # 4. 安全计算
        try:
            res = eval(expr, {"__builtins__": None}, safe_env)
            # 过滤非数值结果（复数、非数字等）
            if not isinstance(res, (int, float)):
                print("WRONG")
            else:
                print("{0:.2f}".format(res))
        except Exception:
            # 所有错误统一输出 WRONG
            print("WRONG")

if __name__ == "__main__":
    main()
