# External reference: http://cs101.openjudge.cn/practice/27925/statistics/
# Accepted submission: 52723049
# Source: http://cs101.openjudge.cn/practice/solution/52723049/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import deque
def main():
    data = sys.stdin.read().splitlines()
    t = int(data[0])
    ptr = 1
    person_to_group = {}
    group_queue = {}
    main_queue = deque()
    group_id = 0
    for _ in range(t):
        members = list(map(int, data[ptr].split()))
        ptr += 1
        group_queue[group_id] = deque()
        for p in members:
            person_to_group[p] = group_id
        group_id += 1
    while ptr < len(data):
        line = data[ptr].strip()
        ptr += 1
        if not line:
            continue
        cmd = line.split()
        if cmd[0] == 'STOP':
            break
        elif cmd[0] == 'ENQUEUE':
            x = int(cmd[1])
            if x not in person_to_group:
                g = -x
                group_queue[g] = deque([x])
                main_queue.append(g)
            else:
                g = person_to_group[x]
                if not group_queue[g]:
                    main_queue.append(g)
                group_queue[g].append(x)
        elif cmd[0] == 'DEQUEUE':
            cur_g = main_queue[0]
            out_p = group_queue[cur_g].popleft()
            print(out_p)
            if not group_queue[cur_g]:
                main_queue.popleft()
if __name__ == '__main__':
    main()
