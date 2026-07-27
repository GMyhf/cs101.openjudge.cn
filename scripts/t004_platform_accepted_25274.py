# External reference: statistics page /practice/25274/
# Accepted submission: 52740084
# Source: http://cs101.openjudge.cn/practice/solution/52740084/
# License: not declared on the submission page; no license is inferred.

import copy

# 原始列表
lst = [[1, 2, 3], 'abc', [1, 3], 4]

# 1.赋值
assign = lst
# 2.浅拷贝
shallow = copy.copy(lst)
# 3.深拷贝
deep = copy.deepcopy(lst)

# 按题目执行修改
lst[0].append(4)
lst[1] = 'def'
lst.append(5)

# 依次输出三行
print(assign)
print(shallow)
print(deep)