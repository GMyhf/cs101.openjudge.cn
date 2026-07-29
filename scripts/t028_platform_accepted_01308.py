# External reference: http://cs101.openjudge.cn/practice/01308/statistics/
# Accepted submission: 52642572
# Source: http://cs101.openjudge.cn/practice/solution/52642572/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import defaultdict, deque
def main():
    inputs = map(int, sys.stdin.read().split())
    cases = 0
    adj = defaultdict(list)
    indegree = defaultdict(int)
    keys = set()

    while True:
        u = next(inputs)
        v = next(inputs)

        flag = True
        if u == -1 and v == -1:
            return

        elif u == 0 and v == 0:
            cases += 1
            root = None
            for key in keys:
                if indegree[key] == 0 and root is None:
                    root = key
                elif indegree[key] == 0:
                    flag = False
                    break
                elif indegree[key] > 1:
                    flag = False
                    break
            if root is None:
                flag = False

            if flag:
                visited = set([root])
                queue = deque([root])
                while queue:
                    curr = queue.popleft()
                    neighbour = adj[curr]
                    for nei in neighbour:
                        if nei in visited:
                            flag = False
                            break
                        queue.append(nei)
                        visited.add(nei)
            if len(visited) < len(keys):
                flag = False

            if not keys:
                flag = True

            if flag:
                print(f"Case {cases} is a tree.")
            else:
                print(f"Case {cases} is not a tree.")
            adj = defaultdict(list)
            indegree = defaultdict(int)
            keys = set()

        else:
            adj[u].append(v)
            keys.add(u)
            keys.add(v)
            indegree[v] += 1

if __name__ == "__main__":
    main()
