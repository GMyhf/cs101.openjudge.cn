# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 3151: Pots
# Fenced code block index: None
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/03151/
# License: not declared in source collection; no license is inferred.
import sys
from collections import deque
A,B,C=map(int,input().split());q=deque([(0,0)]);prev={(0,0):None};how={}
while q:
 x,y=q.popleft()
 if x==C or y==C:
  out=[]
  while prev[(x,y)] is not None:out.append(how[(x,y)]);x,y=prev[(x,y)]
  print(len(out));print('\n'.join(reversed(out)));break
 z=min(x,B-y);w=min(y,A-x)
 for state,op in [((A,y),'FILL(1)'),((x,B),'FILL(2)'),((0,y),'DROP(1)'),((x,0),'DROP(2)'),((x-z,y+z),'POUR(1,2)'),((x+w,y-w),'POUR(2,1)')]:
  if state not in prev:prev[state]=(x,y);how[state]=op;q.append(state)
else:print('impossible')
