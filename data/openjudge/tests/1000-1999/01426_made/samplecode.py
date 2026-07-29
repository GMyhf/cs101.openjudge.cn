# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1426: Find The Multiple
# Fenced code block index: None
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01426/
# License: not declared in source collection; no license is inferred.
import sys
from collections import deque
for line in sys.stdin:
 n=int(line)
 if n==0: break
 q=deque([1%n]); parent={1%n:(None,'1')}
 while q:
  x=q.popleft()
  if x==0: break
  for d in '01':
   y=(x*10+int(d))%n
   if y not in parent: parent[y]=(x,d);q.append(y)
 out=[];x=0
 while x is not None: x,d=parent[x];out.append(d)
 print(''.join(reversed(out)))
