def solve(text):
    values = list(map(int, text.split())); preorder = values[1:]; postorder = []
    def visit(sequence):
        if not sequence: return
        root = sequence[0]; cut = 1
        while cut < len(sequence) and sequence[cut] < root: cut += 1
        visit(sequence[1:cut]); visit(sequence[cut:]); postorder.append(str(root))
    visit(preorder)
    return " ".join(postorder) + "\n"


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
