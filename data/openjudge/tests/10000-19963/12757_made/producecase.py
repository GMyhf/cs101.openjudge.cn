import random, subprocess, tempfile
from pathlib import Path
SAMPLE_IN = 'negative seven hundred twenty nine\n'
SAMPLE_OUT = '-729\n'
CASES = ['negative seven hundred twenty nine\n', 'seven million three hundred ninety two thousand four hundred forty four\n', 'one million eight hundred seventy three thousand six hundred thirty four\n', 'six million three hundred twenty nine thousand two hundred twenty eight\n', 'two million six hundred twenty two thousand five hundred twenty nine\n', 'eight million eighty two thousand nineteen\n', 'negative five million five hundred fifty five thousand three hundred twenty eight\n', 'one million seven hundred eighty three thousand two hundred sixteen\n', 'negative five million seven hundred seventy eight thousand seven hundred seventy three\n', 'eight million nine hundred two thousand seven hundred twenty six\n', 'one million twenty six thousand four hundred sixty seven\n', 'eight hundred eighty three thousand six hundred sixty five\n', 'one million seven hundred ten thousand four hundred seventy seven\n', 'nine million one hundred four thousand five hundred twelve\n', 'negative six million nine hundred ninety one thousand one hundred ninety seven\n', 'six million nine hundred two thousand one hundred seventy three\n', 'six million eight hundred eighteen thousand three hundred thirty nine\n', 'negative seven million one hundred sixty five thousand eight hundred thirteen\n', 'negative six million eight hundred thirty five thousand four hundred ninety five\n', 'two million six hundred fifty seven thousand two hundred thirty three\n']
REFERENCE_SOURCE = '# 焦玮宸 24数学科学学院\ndictionary = {\'zero\': 0, \'one\': 1, \'two\': 2, \'three\': 3, \'four\': 4, \'five\': 5, \'six\': 6, \'seven\': 7, \'eight\': 8, \'nine\': 9, \'ten\': 10, \'eleven\': 11, \'twelve\': 12, \'thirteen\': 13, \'fourteen\': 14, \'fifteen\': 15, \'sixteen\': 16, \'seventeen\': 17, \'eighteen\': 18, \'nineteen\': 19, \'twenty\': 20, \'thirty\': 30, \'forty\': 40, \'fifty\': 50, \'sixty\': 60, \'seventy\': 70, \'eighty\': 80, \'ninety\': 90}\ndef convert(words):\n    if words[0] == "negative":\n        return -convert(words[1:])\n    if "million" in words:\n        ind = words.index("million")\n        return convert(words[:ind]) * (10 ** 6) + (convert(words[ind + 1:]) if ind < len(words) - 1 else 0)\n    if "thousand" in words:\n        ind = words.index("thousand")\n        return convert(words[:ind]) * (10 ** 3) + (convert(words[ind + 1:]) if ind < len(words) - 1 else 0)\n    if "hundred" in words:\n        ind = words.index("hundred")\n        return convert(words[:ind]) * (10 ** 2) + (convert(words[ind + 1:]) if ind < len(words) - 1 else 0)\n    return sum(list(map(lambda s: dictionary[s], words)))\n\n\nprint(convert(list(input().split())))\n'
assert CASES[0] == SAMPLE_IN
random.seed(12757)
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
root = Path(__file__).parent / "data"
for index, content in enumerate(CASES):
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")
