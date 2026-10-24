"""审核用语义校验：接受所有最优树标号、所有连接词排列，不修改题库接入。"""
from collections import deque
from functools import lru_cache
from pathlib import Path
import sys


def mex_tree(given, actual):
    try:
        values=list(map(int,given.split()));n=values[0]
        if not 1<=n<=10000 or len(values)!=2*n-1:return False
        edges=list(zip(values[1::2],values[2::2]));adj=[[] for _ in range(n)]
        parent=list(range(n))
        def find(x):
            while parent[x]!=x:
                parent[x]=parent[parent[x]];x=parent[x]
            return x
        for a,b in edges:
            a-=1;b-=1
            if not 0<=a<n or not 0<=b<n:return False
            u,v=find(a),find(b)
            if u==v:return False
            parent[v]=u;adj[a].append(b);adj[b].append(a)
        labels=list(map(int,actual.split()))
        if len(labels)!=n-1 or set(labels)!=set(range(n-1)):return False
        degree=list(map(len,adj))
        # 路径树的任意排列均达到最优n−1；分叉树的最优值为2。
        if max(degree,default=0)<=2:return True
        marked=set()
        for label in range(3):
            a,b=edges[labels.index(label)];marked.update((a-1,b-1))
        alive=[True]*n
        queue=deque(i for i in range(n) if degree[i]<=1 and i not in marked)
        while queue:
            v=queue.popleft()
            if not alive[v]:continue
            alive[v]=False
            for u in adj[v]:
                if alive[u]:
                    degree[u]-=1
                    if degree[u]==1 and u not in marked:queue.append(u)
        # 三条低标号边的最小连接子树有分叉，等价于不存在路径同时含0/1/2。
        return any(alive[i] and degree[i]>=3 for i in range(n))
    except (ValueError,IndexError,TypeError):
        return False


def concatenated_words(given,actual):
    words=given.split()
    if not 1<=len(words)<=10000 or len(set(words))!=len(words):return False
    if any(not 1<=len(w)<=30 or any(not 'a'<=c<='z' for c in w) for w in words):return False
    trie={}
    for word in words:
        node=trie
        for c in word:node=node.setdefault(c,{})
        node['']=True
    expected=set()
    for word in words:
        @lru_cache(None)
        def split_from(start):
            node=trie
            for i in range(start,len(word)):
                node=node.get(word[i])
                if node is None:return False
                if '' in node:
                    if i+1==len(word):return start>0
                    if split_from(i+1):return True
            return False
        if split_from(0):expected.add(word)
    output=actual.split()
    if not expected:return output==['None']
    return len(output)==len(expected) and set(output)==expected


def validate(number,given,actual):
    return {27952:mex_tree,28341:concatenated_words}[number](given,actual)


def checker_main(number):
    if len(sys.argv)!=4:raise SystemExit(1)
    given=Path(sys.argv[1]).read_text()
    try:actual=Path(sys.argv[2]).read_text()
    except UnicodeError:raise SystemExit(42)
    raise SystemExit(0 if validate(number,given,actual) else 42)
