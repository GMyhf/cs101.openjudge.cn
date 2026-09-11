import sys

def solve(text):
    v = list(map(int, text.split()));
    if not v: return ''
    n, target = v[0], v[1:]
    if len(target) != n: return 'NO\n'
    stack = []; next_value = 1; out = []
    for wanted in target:
        while next_value <= n and (not stack or stack[-1] != wanted):
            stack.append(next_value); out.append(f'PUSH {next_value}'); next_value += 1
        if not stack or stack[-1] != wanted: return 'NO\n'
        stack.pop(); out.append(f'POP {wanted}')
    return '\n'.join(out) + '\n'

if __name__ == '__main__': sys.stdout.write(solve(sys.stdin.read()))
