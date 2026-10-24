"""31381：输出必须是输入字符串的排列，保留空格及字符出现次数。

用法：python3 -I checker.py <输入> <学生输出> <参考答案>。
退出码0通过、42答案错误、3输入数据有误；消息不包含测试内容。
仅允许末尾一个LF或CRLF，不允许额外行。按UTF-8字符计数，不作Unicode归一化。
可直接从输入判断合法性，因此不依赖第三个参数中的参考答案。
"""
from collections import Counter
from pathlib import Path
import sys

MAX_OUTPUT_BYTES = 2 * 1024 * 1024


def one_line(text):
    """仅移除一个行结束符；空格、制表符和Unicode分隔符均是字符串字符。"""
    if text.endswith('\r\n'):
        text = text[:-2]
    elif text.endswith('\n'):
        text = text[:-1]
    if '\n' in text or '\r' in text:
        raise ValueError('必须恰好一行')
    return text


def matches(given, actual):
    return Counter(given) == Counter(actual)


def main():
    if len(sys.argv) != 4:
        print('用法：checker.py 输入 学生输出 参考答案', file=sys.stderr)
        return 3
    try:
        given = one_line(Path(sys.argv[1]).read_bytes().decode('utf-8'))
    except (UnicodeError, ValueError):
        print('判题输入格式有误')
        return 3
    with open(sys.argv[2], 'rb') as handle:
        raw = handle.read(MAX_OUTPUT_BYTES + 1)
    if len(raw) > MAX_OUTPUT_BYTES:
        print('输出过长')
        return 42
    try:
        actual = one_line(raw.decode('utf-8'))
    except (UnicodeError, ValueError):
        print('输出必须是一行UTF-8字符串')
        return 42
    if not matches(given, actual):
        print('输出字符及其出现次数必须与输入一致')
        return 42
    return 0


if __name__ == '__main__':
    sys.exit(main())
