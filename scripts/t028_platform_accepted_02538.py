# External reference: http://cs101.openjudge.cn/practice/02538/statistics/
# Accepted submission: 51766151
# Source: http://cs101.openjudge.cn/practice/solution/51766151/
# License: not declared on the submission page; no license is inferred.

import sys
def main():
    mapping = {
        '1': '`', '2': '1', '3': '2', '4': '3', '5': '4',
        '6': '5', '7': '6', '8': '7', '9': '8', '0': '9',
        '-': '0', '=': '-',
        'W': 'Q', 'E': 'W', 'R': 'E', 'T': 'R', 'Y': 'T',
        'U': 'Y', 'I': 'U', 'O': 'I', 'P': 'O',
        '[': 'P', ']': '[', '\\': ']',
        'S': 'A', 'D': 'S', 'F': 'D', 'G': 'F', 'H': 'G',
        'J': 'H', 'K': 'J', 'L': 'K',
        ';': 'L', "'": ';',
        'X': 'Z', 'C': 'X', 'V': 'C', 'B': 'V', 'N': 'B',
        'M': 'N', ',': 'M', '.': ',', '/': '.'
    }
    for line in sys.stdin:
        if not line.strip():
            print()
            continue
        result = []
        for ch in line.rstrip('\n'):
            if ch == ' ':
                result.append(' ')
            elif ch in mapping:
                result.append(mapping[ch])
            else:
                result.append(ch)
        print(''.join(result))
if __name__ == "__main__":
    main()
