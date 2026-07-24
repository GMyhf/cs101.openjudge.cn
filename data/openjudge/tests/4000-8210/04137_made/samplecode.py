def solve(text):
    it = iter(text.split()); out = []
    for _ in range(int(next(it))):
        number, remove = next(it), int(next(it)); stack = []
        for ch in number:
            while stack and remove and stack[-1] > ch:
                stack.pop(); remove -= 1
            stack.append(ch)
        if remove: stack = stack[:-remove]
        out.append("".join(stack).lstrip("0") or "0")
    return "\n".join(out) + "\n"


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
