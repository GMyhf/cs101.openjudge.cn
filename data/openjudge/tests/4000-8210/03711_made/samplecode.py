# LLM-written reference implementation
import sys
a,b=sys.stdin.read().split()
if len(a)<len(b): a,b=b,a
print("true" if b in a+a else "false")