"""仅用于只读复核题面契约，不替换或放宽现有valid()。"""
import unittest


def statement_contract(number,payload):
    try:
        values=list(map(int,payload.split()));n=values[0];data=values[1:]
        if number==19962:return 1<=n<=100000 and len(data)==n and all(1<=v<=100000 for v in data)
        if number==25570:return 1<=n<=100 and len(data)==n*n and all(0<=v<=10000 for v in data)
        if number==28013:return 1<=n<=1000 and len(data)==n and len(set(data))==n
        if number==30930:return 1<=n<=500000 and len(data)==n and all(0<=v<=10**9 for v in data)
    except (ValueError,IndexError):return False
    raise ValueError('未知题号')


class ContractRecheckTests(unittest.TestCase):
    def test_coordinate_bounds_are_in_description(self):
        self.assertTrue(statement_contract(19962,b'3\n1 100000 10\n'))
        self.assertFalse(statement_contract(19962,b'3\n1 100001 10\n'))
        self.assertFalse(statement_contract(19962,b'1\n0\n'))
        self.assertFalse(statement_contract(19962,b'3\n1 2'))
    def test_matrix_trailing_blank_line_is_whitespace(self):
        self.assertTrue(statement_contract(25570,b'2\n0 10000\n7 2\n\n'))
        self.assertFalse(statement_contract(25570,b'2\n0 10001\n7 2\n'))
        self.assertFalse(statement_contract(25570,b'2\n1 2\n3\n'))
    def test_heap_labels_are_distinct_integers_including_zero(self):
        self.assertTrue(statement_contract(28013,b'3\n0 -1 10000000000\n'))
        self.assertFalse(statement_contract(28013,b'3\n0 1 1\n'))
    def test_chat_blank_lines_do_not_change_count_or_range(self):
        self.assertTrue(statement_contract(30930,b'3\n0 1 1000000000\n\n'))
        self.assertFalse(statement_contract(30930,b'3\n0 1 1000000001\n'))
        self.assertFalse(statement_contract(30930,b'3\n0 1\n'))
