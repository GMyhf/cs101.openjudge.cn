# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1852: Ants
# Fenced code block index: None
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/01852/
# License: not declared in source collection; no license is inferred.
import sys
a=list(map(int,sys.stdin.buffer.read().split()));p=1
for _ in range(a[0]):
 L,n=a[p:p+2];p+=2;x=a[p:p+n];p+=n
 print(max(min(v,L-v) for v in x),max(max(v,L-v) for v in x))
