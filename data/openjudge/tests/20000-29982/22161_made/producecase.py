import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "import heapq\n\nclass Node:\n    def __init__(self, weight, char=None):\n        self.weight = weight\n        self.char = char\n        self.left = None\n        self.right = None\n\n    def __lt__(self, other):\n        if self.weight == other.weight:\n            return self.char < other.char\n        return self.weight < other.weight\n\ndef build_huffman_tree(characters):\n    heap = []\n    for char, weight in characters.items():\n        heapq.heappush(heap, Node(weight, char))\n\n    while len(heap) > 1:\n        left = heapq.heappop(heap)\n        right = heapq.heappop(heap)\n        merged = Node(left.weight + right.weight)\n        merged.left = left\n        merged.right = right\n        heapq.heappush(heap, merged)\n\n    return heap[0]\n\ndef encode_huffman_tree(root):\n    codes = {}\n\n    def traverse(node, code):\n        if node.char:\n            codes[node.char] = code\n        else:\n            traverse(node.left, code + '0')\n            traverse(node.right, code + '1')\n\n    traverse(root, '')\n    return codes\n\ndef huffman_encoding(codes, string):\n    encoded = ''\n    for char in string:\n        encoded += codes[char]\n    return encoded\n\ndef huffman_decoding(root, encoded_string):\n    decoded = ''\n    node = root\n    for bit in encoded_string:\n        if bit == '0':\n            node = node.left\n        else:\n            node = node.right\n\n        if node.char:\n            decoded += node.char\n            node = root\n    return decoded\n\n# 读取输入\nn = int(input())\ncharacters = {}\nfor _ in range(n):\n    char, weight = input().split()\n    characters[char] = int(weight)\n\n#string = input().strip()\n#encoded_string = input().strip()\n\n# 构建哈夫曼编码树\nhuffman_tree = build_huffman_tree(characters)\n\n# 编码和解码\ncodes = encode_huffman_tree(huffman_tree)\n\nstrings = []\nwhile True:\n    try:\n        line = input()\n        if line:\n            strings.append(line)\n        else:\n            break\n    except EOFError:\n        break\n\nresults = []\n#print(strings)\nfor string in strings:\n    if string[0] in ('0','1'):\n        results.append(huffman_decoding(huffman_tree, string))\n    else:\n        results.append(huffman_encoding(codes, string))\n\nfor result in results:\n    print(result)\n"
SAMPLE_IN = '3\ng 4\nd 8\nc 10\ndc\n110\n'
SAMPLE_OUT = '110\ndc\n'
def generate_case(r):
    chars = r.sample("abcdefghi", r.randint(3, 6)); lines = [str(len(chars))]
    weights = [2 ** (i * 4) for i in range(len(chars))]
    assert len(set(chars)) == len(chars) and len(set(weights)) == len(weights)
    for c, weight in zip(chars, weights): lines.append(f"{c} {weight}")
    words = ["".join(r.choice(chars) for _ in range(r.randint(1, 8))) for _ in range(3)]
    return "\n".join(lines + words) + "\n"

assert SAMPLE_IN == '3\ng 4\nd 8\nc 10\ndc\n110\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(22161 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
