def build_preorder(inorder, postorder):
    if not inorder or not postorder:
        return []

    root = postorder[-1]  # 后序遍历的最后一个节点是根节点
    root_index = inorder.index(root)  # 在中序遍历中找到根节点

    # 递归构造左子树和右子树的前序遍历
    left_preorder = build_preorder(inorder[:root_index], postorder[:root_index])
    right_preorder = build_preorder(inorder[root_index + 1:], postorder[root_index:-1])

    return [root] + left_preorder + right_preorder 


inorder = list(map(int, input().split())) 
postorder = list(map(int, input().split()))  
preorder = build_preorder(inorder, postorder)
print(*preorder)