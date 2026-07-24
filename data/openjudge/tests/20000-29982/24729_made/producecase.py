import random
import time
import os
import string

# 确保 data 目录存在
os.makedirs("data", exist_ok=True)

# --- AC.PY 中的逻辑 ---
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

def parse_tree(s):
    stack = []
    node = None
    for char in s:
        if char.isalpha():
            node = TreeNode(char)
            if stack:
                stack[-1].children.append(node)
        elif char == '(':
            if node:
                stack.append(node)
                node = None
        elif char == ')':
            if stack:
                node = stack.pop()
    return node

def preorder(node):
    if not node: return ""
    output = [node.value]
    for child in node.children:
        output.extend(preorder(child))
    return ''.join(output)

def postorder(node):
    if not node: return ""
    output = []
    for child in node.children:
        output.extend(postorder(child))
    output.append(node.value)
    return ''.join(output)

def solve(s):
    s = ''.join(s.split())
    root = parse_tree(s)
    if root:
        return [preorder(root), postorder(root)]
    return []

# --- 随机树生成逻辑 ---
class GenNode:
    def __init__(self, val):
        self.val = val
        self.children = []

def serialize(node):
    if not node.children:
        return node.val
    children_s = ",".join(serialize(child) for child in node.children)
    return f"{node.val}({children_s})"

def generate_random_tree_string(node_count):
    if node_count <= 0: return ""
    labels = list(string.ascii_uppercase)
    random.shuffle(labels)
    used_labels = labels[:node_count]
    
    nodes = [GenNode(used_labels[0])]
    for i in range(1, node_count):
        new_node = GenNode(used_labels[i])
        # 随机选一个已有的节点作为父节点
        parent = random.choice(nodes)
        parent.children.append(new_node)
        nodes.append(new_node)
    
    return serialize(nodes[0])

# --- 主生成循环 ---
for epoch in range(30):
    # 针对不同规模生成数据
    if epoch == 0:
        # 边界情况：只有一个节点
        tree_str = "A"
    elif epoch < 5:
        # 小规模
        tree_str = generate_random_tree_string(random.randint(2, 5))
    elif epoch < 10:
        # 链状树（深）
        labels = list(string.ascii_uppercase[:random.randint(10, 26)])
        tree_str = labels[-1]
        for i in range(len(labels)-2, -1, -1):
            tree_str = f"{labels[i]}({tree_str})"
    else:
        # 随机中大规模
        tree_str = generate_random_tree_string(random.randint(10, 26))

    # 写入输入文件
    with open(f"data/{epoch}.in", "w") as f:
        f.write(tree_str + "\n")

    start = time.time()

    # 调用 AC 逻辑计算答案
    result = solve(tree_str)

    end = time.time() - start
    print(f"[{epoch}] {end:.3f}s | nodes={len(tree_str.replace('(','').replace(')','').replace(',',''))}")

    # 写入输出文件
    with open(f"data/{epoch}.out", "w") as f:
        if result:
            f.write("\n".join(result) + "\n")
