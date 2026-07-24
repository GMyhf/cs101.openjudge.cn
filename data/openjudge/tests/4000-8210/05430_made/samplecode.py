# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
'''
表达式树是一种特殊的二叉树。对于你的问题，需要先将中缀表达式转换为后缀表达式
（逆波兰式），然后根据后缀表达式建立表达式树，最后进行计算。

首先使用stack进行中缀到后缀的转换，然后根据后缀表达式建立表达式二叉树，
再通过递归和映射获取表达式的值。
最后，打印出整棵树（取自 23n2300017735，夏天明BrightSummer）

中缀表达式转后缀表达式 https://zq99299.github.io/dsalg-tutorial/dsalg-java-hsp/05/05.html
'''
#from collections import deque as q
import operator as op
#import os


class Node:
    def __init__(self, x):
        self.value = x
        self.left = None
        self.right = None


def priority(x):
    if x == '*' or x == '/':
        return 2
    if x == '+' or x == '-':
        return 1
    return 0


def infix_trans(infix):
    postfix = []
    op_stack = []
    for char in infix:
        if char.isalpha():
            postfix.append(char)
        else:
            if char == '(':
                op_stack.append(char)
            elif char == ')':
                while op_stack and op_stack[-1] != '(':
                    postfix.append(op_stack.pop())
                op_stack.pop()
            else:
                while op_stack and priority(op_stack[-1]) >= priority(char) and op_stack[-1] != '(':
                    postfix.append(op_stack.pop())
                op_stack.append(char)
    while op_stack:
        postfix.append(op_stack.pop())
    return postfix


def build_tree(postfix):
    stack = []
    for item in postfix:
        if item in '+-*/':
            node = Node(item)
            node.right = stack.pop()
            node.left = stack.pop()
        else:
            node = Node(item)
        stack.append(node)
    return stack[0]


def get_val(expr_tree, var_vals):
    if expr_tree.value in '+-*/':
        operator = {'+': op.add, '-': op.sub, '*': op.mul, '/': op.floordiv}
        return operator[expr_tree.value](get_val(expr_tree.left, var_vals), get_val(expr_tree.right, var_vals))
    else:
        return var_vals[expr_tree.value]

# 计算表达式树的深度。它通过递归地计算左右子树的深度，并取两者中的最大值再加1，得到整个表达式树的深度。


def getDepth(tree_root):
    #return max([self.child[i].getDepth() if self.child[i] else 0 for i in range(2)]) + 1
    left_depth = getDepth(tree_root.left) if tree_root.left else 0
    right_depth = getDepth(tree_root.right) if tree_root.right else 0
    return max(left_depth, right_depth) + 1

    '''
    首先，根据表达式树的值和深度信息构建第一行，然后构建第二行，该行包含斜线和反斜线，
    用于表示子树的链接关系。接下来，如果当前深度为0，表示已经遍历到叶子节点，直接返回该节点的值。
    否则，递减深度并分别获取左子树和右子树的打印结果。最后，将左子树和右子树的每一行拼接在一起，
    形成完整的树形打印图。
    
打印表达式树的函数。表达式树是一种抽象数据结构，它通过树的形式来表示数学表达式。在这段程序中，
函数printExpressionTree接受两个参数：tree_root表示树的根节点，d表示树的总深度。
首先，函数会创建一个列表graph，列表中的每个元素代表树的一行。第一行包含根节点的值，
并使用空格填充左右两边以保持树的形状。第二行显示左右子树的链接情况，使用斜杠/表示有左子树，
反斜杠\表示有右子树，空格表示没有子树。

接下来，函数会判断深度d是否为0，若为0则表示已经达到树的最底层，直接返回根节点的值。否则，
将深度减1，然后递归调用printExpressionTree函数打印左子树和右子树，
并将结果分别存储在left和right中。

最后，函数通过循环遍历2倍深度加1次，将左子树和右子树的每一行连接起来，存储在graph中。
最后返回graph，即可得到打印好的表达式树。
    '''


def printExpressionTree(tree_root, d):  # d means total depth

    graph = [" "*(2**d-1) + tree_root.value + " "*(2**d-1)]
    graph.append(" "*(2**d-2) + ("/" if tree_root.left else " ")
                 + " " + ("\\" if tree_root.right else " ") + " "*(2**d-2))

    if d == 0:
        return tree_root.value
    d -= 1
    '''
    应该是因为深度每增加一层，打印宽度就增加一倍，打印行数增加两行
    '''
    #left = printExpressionTree(tree_root.left, d) if tree_root.left else [
    #    " "*(2**(d+1)-1)]*(2*d+1)
    if tree_root.left:
        left = printExpressionTree(tree_root.left, d)
    else:
        #print("left_d",d)
        left = [" "*(2**(d+1)-1)]*(2*d+1)
        #print("left_left",left)

    right = printExpressionTree(tree_root.right, d) if tree_root.right else [
        " "*(2**(d+1)-1)]*(2*d+1)

    for i in range(2*d+1):
        graph.append(left[i] + " " + right[i])
        #print('graph=',graph)
    return graph



infix = input().strip()
n = int(input())
vars_vals = {}
for i in range(n):
    line = input().split()
    vars_vals[line[0]] = int(line[1])
    
'''
infix = "a+(b-c*d*e)"
#infix = "a+b*c"
n = 5
vars_vals = {'a': 2, 'b': 7, 'c': 5, 'd':1, 'e':1}
'''

postfix = infix_trans(infix)
tree_root = build_tree(postfix)
print(''.join(str(x) for x in postfix))
expression_value = get_val(tree_root, vars_vals)


for line in printExpressionTree(tree_root, getDepth(tree_root)-1):
    print(line.rstrip())


print(expression_value)
