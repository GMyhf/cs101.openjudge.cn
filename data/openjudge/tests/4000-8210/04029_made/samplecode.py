# T-004-r2 reference implementation
import sys
s=sys.stdin.read().strip()
sign="-" if s.startswith("-") else ""
digits=s[1:] if sign else s
print(sign + digits[::-1].lstrip("0") or "0")