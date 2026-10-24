#!/usr/bin/env python3
"""31028—31032的完整平台数据：300万行i；超本地2MiB上限，不接入本地判题。

生成物只写到--work指定目录；仓库保存生成器和哈希回执，不提交约22MiB的答案。
合法输入只有这一份，不用缩小行数或重复样例凑20组。
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

NUMBERS = tuple(range(31028, 31033))
COUNT = 3_000_000
EXPECTED_BYTES = 22_888_896
REFERENCE_SOURCE = '''"""仓库自产参考：按块原样复制完整输入，不改变平台测试规模。"""
import sys
while True:
    block=sys.stdin.buffer.read(65536)
    if not block:break
    sys.stdout.buffer.write(block)
'''


def chunks(count=COUNT):
    """按固定块生成十进制行；count参数只供离线小范围校准。"""
    for start in range(1, count + 1, 10000):
        yield ''.join(f'{i}\n' for i in range(start, min(start + 10000, count + 1))).encode()


def validate_file(path):
    """独立逐行检查，不把大文件作为一个字符串载入内存。"""
    with Path(path).open('rb') as stream:
        for expected in range(1, COUNT + 1):
            if stream.readline() != str(expected).encode() + b'\n':
                return False
        return stream.read(1) == b''


def digest(path):
    hasher=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(65536), b''):
            hasher.update(block)
    return hasher.hexdigest()


def build(work):
    work=Path(work);work.mkdir(parents=True,exist_ok=True)
    given=work/'0.in';answer=work/'0.out'
    with given.open('wb') as stream:
        for block in chunks():stream.write(block)
    if given.stat().st_size != EXPECTED_BYTES or not validate_file(given):
        raise ValueError('300万行输入校验失败')
    shutil.copyfile(given,answer)
    if digest(given)!=digest(answer):raise ValueError('原样输出校验失败')
    (work/'samplecode.py').write_text(REFERENCE_SOURCE)
    manifest={'problems':list(NUMBERS),'cases_per_problem':1,'lines':COUNT,
              'bytes_per_file':EXPECTED_BYTES,'local_enabled':False,
              'reason':'完整答案超过本地2MiB上限；只补平台完整数据，不截短原题。',
              'files':[{'filename':p.name,'bytes':p.stat().st_size,'sha256':digest(p)} for p in (given,answer)]}
    (work/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    return manifest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work',type=Path,required=True)
    args=parser.parse_args();print(json.dumps(build(args.work),ensure_ascii=False))


if __name__=='__main__':main()
