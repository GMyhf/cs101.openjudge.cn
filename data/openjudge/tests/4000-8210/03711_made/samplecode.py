# LLM-written reference implementation
import sys
a,b=sys.stdin.read().split()
print("true" if a in b+b or b in a+a else "false")