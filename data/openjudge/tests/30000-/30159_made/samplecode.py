# External reference: http://cs101.openjudge.cn/practice/30159/statistics/
# Accepted submission: 52997416
# Source: http://cs101.openjudge.cn/practice/solution/52997416/
# License: not declared on the submission page; no license is inferred.

import itertools
import sys
from functools import reduce
from operator import and_, or_


class LazyDelete:
    def __init__(self, arr: list):
        self.arr = arr
        self.length = len(arr)
        self.prev = [self.length] + list(range(0,self.length))
        self.succ = list(range(1,self.length + 1)) + [0]

    def __iter__(self):
        i = self.succ[self.length]
        while i != self.length:
            yield self.arr[i]
            i = self.succ[i]

    def filter(self, func, *args, **kwargs) -> None:
        i = self.succ[self.length]
        while i != self.length:
            if not func(self.arr[i], *args, **kwargs):
                self.succ[self.prev[i]] = self.succ[i]
                self.prev[self.succ[i]] = self.prev[i]
            i = self.succ[i]


def generate_all(arr: list, length: int) -> LazyDelete:
    sep = len(arr) + 1
    blank = length - sum(arr) - len(arr) + 1
    elem = [(1 << i) - 1 for i in arr]
    comb = itertools.combinations_with_replacement(range(sep), blank)
    entire = []
    for i in comb:
        this = 0
        cursor = 0
        counter = [0] * sep
        for s in i:
            counter[s] += 1
        for j in range(len(arr)):
            cursor += counter[j]
            if j > 0: cursor += 1
            this |= elem[j] << cursor
            cursor += arr[j]
        entire.append(this)
    return LazyDelete(entire)


def find_must(entire: list) -> tuple:
    must_filled = reduce(and_, entire)  # 1 if must filled
    must_empty = reduce(or_, entire)  # 0 if must empty
    return must_filled, must_empty

def meet_condition(psb: int, must_filled: int, must_empty: int) -> bool:
    return not ((~psb & must_filled) or (psb & ~must_empty))


class Nonogram:
    def __init__(self, rows_cond, cols_cond) -> None:
        self.rows_cond = rows_cond
        self.cols_cond = cols_cond
        self.height, self.width = len(rows_cond), len(cols_cond)
        self.size = self.height * self.width
        self.mask = (1 << self.size) - 1
        self.board_filled = 0
        self.board_empty = self.mask

        self.rows = [generate_all(i, self.width) for i in rows_cond]
        self.cols = [generate_all(i, self.height) for i in cols_cond]

        self.row_cache = [None] * self.height
        self.col_cache = [None] * self.width

    def get_row(self, r: int):
        if self.row_cache[r] is None:
            self.row_cache[r] = ((self.board_filled >> (r * self.width)) & ((1 << self.width) - 1),
                (self.board_empty >> (r * self.width)) & ((1 << self.width) - 1))
        return self.row_cache[r]

    def get_col(self, c: int):
        if self.col_cache[c] is None:
            must_filled = must_empty = 0
            for r in range(self.height):
                must_filled |= ((self.board_filled >> (r * self.width + c)) & 1) << r
                must_empty |= ((self.board_empty >> (r * self.width + c)) & 1) << r
                self.col_cache[c] = (must_filled, must_empty)
        return self.col_cache[c]

    def set_row(self, r: int, filled: int, empty: int) -> None:
        self.row_cache[r] = None
        self.board_filled &= ~(((1 << self.width) - 1) << (r * self.width))
        self.board_empty &= ~(((1 << self.width) - 1) << (r * self.width))
        self.board_filled |= filled << (r * self.width)
        self.board_empty |= empty << (r * self.width)

    def set_col(self, c: int, filled: int, empty: int) -> None:
        self.col_cache[c] = None
        for r in range(self.height):
            self.board_filled &= ~(1 << (r * self.width + c))
            self.board_empty &= ~(1 << (r * self.width + c))
            self.board_filled |= ((filled >> r) & 1) << (r * self.width + c)
            self.board_empty |= ((empty >> r) & 1) << (r * self.width + c)

    def solve(self):
        while self.board_filled != self.board_empty:
            for i, entire in enumerate(self.rows):
                entire.filter(meet_condition, *self.get_row(i))
                self.set_row(i, *find_must(entire))
            for i, entire in enumerate(self.cols):
                entire.filter(meet_condition, *self.get_col(i))
                self.set_col(i, *find_must(entire))


def main():
    r, c = map(int, input().split())
    rows_cond = [list(map(int, input().split()))[1:] for _ in range(r)]
    cols_cond = [list(map(int, input().split()))[1:] for _ in range(c)]
    board = Nonogram(rows_cond, cols_cond)
    board.solve()
    filled = board.board_filled
    for i in range(board.size):
        sys.stdout.write(str(filled & 1))
        filled >>= 1
        if (i + 1) % board.width == 0:
            sys.stdout.write('\n')


if __name__ == '__main__':
    main()
