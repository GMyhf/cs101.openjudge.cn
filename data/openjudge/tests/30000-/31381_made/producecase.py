"""31381自产数据：原样例加20组排列、重复字符、空白及Unicode场景。"""
import importlib.util
from pathlib import Path
import random
import re
_spec = importlib.util.spec_from_file_location('reference_31381', Path(__file__).with_name('samplecode.py'))
_reference = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_reference)
solve = _reference.solve

SAMPLE_IN = '1234567890qwertyuiopasdfghjklzxcvbnm\n'
SAMPLE_OUT = 'mnbvcxzqwertyuioplkjhgfdsa0987654321\n'
SHAPES = ('a', 'aab', 'abb', 'z'*257, ' aab ', '\taba\t', '甲甲乙乙丙',
          'é e\u0301', '', '   ', 'AaAa00!!', '<>&"\\', '0'*1024, 'ab'*1024,
          '甲\u2028乙\t甲')


def valid(text):
    """题面只要求一行字符串，没有数值或长度范围；不丢弃空白字符。"""
    return isinstance(text, str) and re.fullmatch(r'[^\r\n]*(?:\r?\n)?', text) is not None


def generate(number, seed):
    assert number == 31381 and 1 <= seed <= 20
    if seed <= len(SHAPES):
        return SHAPES[seed-1] + '\n'
    rng = random.Random(number*100+seed)
    alphabet = 'aaaabbCC001! ~\t甲乙é'
    return ''.join(rng.choice(alphabet) for _ in range((seed-15)*347)) + '\n'


def build():
    target = Path(__file__).parent/'data'
    target.mkdir(exist_ok=True)
    seen = set()
    for seed in range(21):
        given = SAMPLE_IN if seed == 0 else generate(31381, seed)
        answer = SAMPLE_OUT if seed == 0 else solve(given)+'\n'
        assert valid(given) and given not in seen
        seen.add(given)
        # 独立排序模型校准反转参考；第0组保留原题样例，不能自行排序替换。
        assert sorted(given[:-1]) == sorted(answer[:-1])
        if seed == 0:
            assert given == SAMPLE_IN and answer == SAMPLE_OUT
        (target/f'{seed}.in').write_bytes(given.encode('utf-8'))
        (target/f'{seed}.out').write_bytes(answer.encode('utf-8'))
    print('31381生成21组互异输入，样例字节与原题保持')


if __name__ == '__main__':
    build()
