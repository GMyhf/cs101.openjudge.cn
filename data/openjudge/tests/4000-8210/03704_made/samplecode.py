# T-004-r3 reference implementation
import sys
for line in sys.stdin.read().splitlines():
    bad=[" "]*len(line); stack=[]
    for i,ch in enumerate(line):
        if ch=="(": stack.append(i)
        elif ch==")":
            if stack: stack.pop()
            else: bad[i]="?"
    for i in stack: bad[i]="$"
    print(line); print("".join(bad).rstrip())