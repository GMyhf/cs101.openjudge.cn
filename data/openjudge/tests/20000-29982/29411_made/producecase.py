import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'class Solution:\n    def intToRoman(self, num: int) -> str:\n        roman_numerals = [\n            (1000, \'M\'), (900, \'CM\'), (500, \'D\'), (400, \'CD\'),\n            (100, \'C\'), (90, \'XC\'), (50, \'L\'), (40, \'XL\'),\n            (10, \'X\'), (9, \'IX\'), (5, \'V\'), (4, \'IV\'), (1, \'I\')\n        ]\n\n        result = []\n        for value, symbol in roman_numerals:\n            while num >= value:\n                result.append(symbol)\n                num -= value\n            if num == 0:\n                break\n\n        return \'\'.join(result)\n\nif __name__ == "__main__":\n    sol = Solution()\n    n = int(input())\n    print(sol.intToRoman(n))\n'
SAMPLE_IN = '3749\n'
def generate_case(r):
    return f"{r.randint(1, 3999)}\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(29411 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
