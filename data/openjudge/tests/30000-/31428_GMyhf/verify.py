"""Verify official bytes and all 100 unique-answer two-sum subcases without generation."""
from collections import defaultdict
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def verify():
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    for name, expected in manifest['files'].items():
        data = (ROOT / 'data' / name).read_bytes()
        assert len(data) == expected['bytes']
        assert hashlib.sha256(data).hexdigest() == expected['sha256']
    lines = (ROOT / 'data/0.in').read_text().splitlines()
    answers = [tuple(map(int, line.split())) for line in (ROOT / 'data/0.out').read_text().splitlines()]
    offset = count = 0
    lengths = []
    while offset < len(lines):
        length, target = map(int, lines[offset].split())
        offset += 1
        if length == target == 0:
            break
        values = list(map(int, lines[offset].split()))
        offset += 1
        assert 2 <= length <= 10000 and len(values) == length
        assert -10**9 <= target <= 10**9
        assert all(-10**9 <= value <= 10**9 for value in values)
        indices = defaultdict(list)
        ways, solution = 0, None
        for j, value in enumerate(values):
            matches = indices.get(target - value, [])
            ways += len(matches)
            if matches:
                solution = (matches[0], j)
            indices[value].append(j)
        assert ways == 1, (count, ways)
        assert answers[count] == solution, (count, answers[count], solution)
        count += 1
        lengths.append(length)
    assert count == len(answers) == manifest['subcases'] == 100
    assert offset == len(lines)
    return {'subcases': count, 'min_length': min(lengths), 'max_length': max(lengths)}


if __name__ == '__main__':
    print(json.dumps(verify()))
