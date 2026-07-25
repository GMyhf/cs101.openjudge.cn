# T-004-r2 reference implementation
import sys
s=sys.stdin.read().strip(); bits=[]
while int(s):
    q,rem=[],0
    for ch in s:
        rem=rem*10+ord(ch)-48
        if q or rem>=2: q.append(str(rem//2)); rem%=2
    s="".join(q) or "0"; bits.append(str(rem))
print("".join(bits[::-1]) or "0")