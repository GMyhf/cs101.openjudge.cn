# LLM-written reference implementation
import sys
a=list(map(int,sys.stdin.read().split()))
print("\n".join(str(bin(x^y).count("1")) for x,y in zip(a[1::2],a[2::2])))