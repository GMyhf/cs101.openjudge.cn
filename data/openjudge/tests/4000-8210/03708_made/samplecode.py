# LLM-written reference implementation
import sys
for x in sys.stdin.read().split()[1:]: print(bin(int(x)).count("1"))