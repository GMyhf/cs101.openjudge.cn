def solve(text):
    n, m = map(int, text.split()); states = [0] * m; states[0] = 1
    for _ in range(n):
        next_states = [0] * m
        for run, count in enumerate(states):
            next_states[0] += count
            if run + 1 < m: next_states[run + 1] += count
        states = next_states
    return str(sum(states)) + "\n"


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
