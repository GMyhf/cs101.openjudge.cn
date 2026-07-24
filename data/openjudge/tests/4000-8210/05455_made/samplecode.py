def solve(text):
    values = list(dict.fromkeys(map(int, text.split())))
    if not values: return ""
    left, right = {}, {}
    for value in values[1:]:
        cur = values[0]
        while True:
            if value < cur:
                if cur not in left: left[cur] = value; break
                cur = left[cur]
            elif value > cur:
                if cur not in right: right[cur] = value; break
                cur = right[cur]
            else: break
    queue = [values[0]]; out = []
    while queue:
        cur = queue.pop(0); out.append(str(cur))
        if cur in left: queue.append(left[cur])
        if cur in right: queue.append(right[cur])
    return " ".join(out) + "\n"


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
