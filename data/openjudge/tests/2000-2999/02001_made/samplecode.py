# External reference: http://cs101.openjudge.cn/practice/02001/statistics/
# Accepted submission: 51717289
# Source: http://cs101.openjudge.cn/practice/solution/51717289/
# License: not declared on the submission page; no license is inferred.

import sys
class TrieNode:
    def __init__(self):
        self.children = {}
        self.count = 0
        self.is_end = False
class Trie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.count += 1
        node.is_end = True
    def shortest_prefix(self, word):
        node = self.root
        prefix = []
        for i, char in enumerate(word):
            node = node.children[char]
            prefix.append(char)
            if node.count == 1:
                return ''.join(prefix)
            if node.is_end and ''.join(prefix) == word:
                return ''.join(prefix)
        return word
words = [line.strip() for line in sys.stdin]
trie = Trie()
for word in words:
    trie.insert(word)
for word in words:
    prefix = trie.shortest_prefix(word)
    print(f'{word} {prefix}')
