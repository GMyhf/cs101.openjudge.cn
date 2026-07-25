# T-004-r3 reference implementation
import sys
out=[]
for line in sys.stdin.read().splitlines():
    parts=line.split()
    if parts and not parts[0].startswith("#") and parts[0]!="":
        out.append(" ".join(parts[1:]))
print(len(out)); print("\n".join(out))