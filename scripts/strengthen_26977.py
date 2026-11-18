#!/usr/bin/env python3
"""为接雨水补充确定性的边界数据；保留 0..21 组平台原件及其来源记录。"""
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'data/openjudge/tests/20000-29982/26977_GMyhf'


def cases():
    return [
        ('严格递减（用户报告 #53919881）', [5, 4, 3, 2, 1]),
        ('严格递增', [1, 2, 3, 4, 5]),
        ('单柱为零', [0]),
        ('单柱最高', [200000]),
        ('两柱递减', [200000, 0]),
        ('两柱递增', [0, 200000]),
        ('全零满规模', [0] * 20000),
        ('等高满规模', [200000] * 20000),
        ('单峰不蓄水', [0, 1, 3, 5, 3, 1, 0]),
        ('不等高边界的盆地', [5, 0, 0, 2]),
        ('连续相等的盆底', [3, 1, 1, 3]),
        ('多个盆地', [5, 0, 5, 0, 5]),
        ('最高柱在中间且两端低', [1, 0, 5, 0, 2]),
        ('蓄水量超过有符号 32 位', [200000] + [0] * 19998 + [200000]),
    ]


def valid(text):
    try:
        lines = text.splitlines()
        n = int(lines[0])
        heights = list(map(int, lines[1].split()))
        return (len(lines) == 2 and 1 <= n <= 20000 and len(heights) == n
                and all(0 <= h <= 200000 for h in heights))
    except (ValueError, IndexError):
        return False


def water(heights):
    """双指针求解；测试另用前后缀最大值独立核对。"""
    left, right = 0, len(heights) - 1
    left_max = right_max = total = 0
    while left <= right:
        if heights[left] <= heights[right]:
            left_max = max(left_max, heights[left])
            total += left_max - heights[left]
            left += 1
        else:
            right_max = max(right_max, heights[right])
            total += right_max - heights[right]
            right -= 1
    return total


def build(directory=DIRECTORY):
    records = []
    for index, (purpose, heights) in enumerate(cases(), 22):
        text = f'{len(heights)}\n' + ' '.join(map(str, heights)) + '\n'
        if not valid(text):
            raise ValueError(f'{index}: 输入越界')
        record = {'case': index, 'purpose': purpose}
        for ext, content in (('in', text), ('out', f'{water(heights)}\n')):
            payload = content.encode()
            (directory / 'data' / f'{index}.{ext}').write_bytes(payload)
            record[ext + '_sha256'] = hashlib.sha256(payload).hexdigest()
        records.append(record)
    (directory / 'SUPPLEMENT.json').write_text(json.dumps({
        'source': '本仓库自造边界数据，非平台原始下载；由 scripts/strengthen_26977.py 生成',
        'reason': '用户报告 #53919881 可能假 A，要求补充递减等边界；实测该提交通过新增数据，尚未复现错误',
        'original_cases': '0..21 保持原始字节，来源及哈希仍见 SOURCE.json',
        'files': records,
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    build()
