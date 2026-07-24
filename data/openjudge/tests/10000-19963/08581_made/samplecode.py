def solve(text):
    preorder = text.strip(); pos = 0; inorder = []; postorder = []
    def visit():
        nonlocal pos
        char = preorder[pos]; pos += 1
        if char == ".": return
        visit(); inorder.append(char); visit(); postorder.append(char)
    visit()
    return "".join(inorder) + "\n" + "".join(postorder) + "\n"


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
