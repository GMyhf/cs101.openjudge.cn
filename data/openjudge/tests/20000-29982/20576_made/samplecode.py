# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
class BinaryTree:
    def __init__(self, root, left=None, right=None):
        self.root = root
        self.leftChild = left
        self.rightChild = right

def postorder(string):  # 中缀改后缀 (Shunting Yard)
    opStack, postList = [], []
    inList = string.split()
    prec = {'(': 0, 'or': 1, 'and': 2, 'not': 3}
    # 定义结合性：L 为左结合，R 为右结合
    assoc = {'or': 'L', 'and': 'L', 'not': 'R'}

    for word in inList:
        if word == '(':
            opStack.append(word)
        elif word == ')':
            while opStack and opStack[-1] != '(':
                postList.append(opStack.pop())
            opStack.pop()
        elif word in ('True', 'False'):
            postList.append(word)
        else:  # operator
            # while opStack and prec[word] <= prec[opStack[-1]]:
            # while opStack and (word != "not" and prec[word] <= prec[opStack[-1]]):
            while (opStack and opStack[-1] in prec and (
                    (assoc[word] == 'L' and prec[word] <= prec[opStack[-1]]) or
                    (assoc[word] == 'R' and prec[word] < prec[opStack[-1]]))):
                postList.append(opStack.pop())
            opStack.append(word)
    while opStack:
        postList.append(opStack.pop())
    return postList

def buildParseTree(infix):
    postList = postorder(infix)
    stack = []
    for word in postList:
        if word == 'not':
            child = stack.pop()
            stack.append(BinaryTree('not', child))
        elif word in ('True', 'False'):
            stack.append(BinaryTree(word))
        else:
            right, left = stack.pop(), stack.pop()
            stack.append(BinaryTree(word, left, right))
    return stack[-1]

# 定义运算符优先级
priority = {'or': 1, 'and': 2, 'not': 3, 'True': 4, 'False': 4}

def printTree(tree):
    """返回 token 列表"""
    root = tree.root
    if root in ('True', 'False'):
        return [root]

    if root == 'not':
        child = tree.leftChild
        # 若子优先级更低则加括号
        child_tokens = printTree(child)
        if priority[child.root] < priority[root]:
            child_tokens = ['('] + child_tokens + [')']
        return ['not'] + child_tokens

    # 二元操作符 and/or
    left, right = tree.leftChild, tree.rightChild
    left_tokens = printTree(left)
    right_tokens = printTree(right)
    if priority[left.root] < priority[root]:
        left_tokens = ['('] + left_tokens + [')']
    if priority[right.root] < priority[root]:
        right_tokens = ['('] + right_tokens + [')']
    return left_tokens + [root] + right_tokens

def main():
    infix = input().strip()
    Tree = buildParseTree(infix)
    print(' '.join(printTree(Tree)))

if __name__ == "__main__":
    main()

