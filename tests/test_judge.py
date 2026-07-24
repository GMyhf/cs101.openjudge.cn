import unittest

from judge import judge


BOOK = "pctbook"
PROBLEM = "E01003"
EXPECTED = """3 card(s)
61 card(s)
1 card(s)
273 card(s)
101 card(s)
2 card(s)
2 card(s)
33 card(s)
102 card(s)
221 card(s)
"""


class JudgeCoreTests(unittest.TestCase):
    def test_accepts_token_equivalent_output(self):
        # The fixture has one input containing the number of days; use the
        # known answer with deliberately different whitespace to exercise the
        # token comparison contract.
        token_output = "  \n".join(line.strip() for line in EXPECTED.splitlines()) + "  \n"
        source = "import sys\nsys.stdout.write(" + repr(token_output) + ")\n"
        result = judge(BOOK, PROBLEM, "python", source)
        self.assertEqual(result["status"], "Accepted")

    def test_wrong_answer_reports_first_case(self):
        source = "print('wrong')\n"
        result = judge(BOOK, PROBLEM, "python", source)
        self.assertEqual(result["status"], "Wrong Answer")
        self.assertEqual(result["case"], 1)

    def test_compile_error_is_distinct_from_runtime_error(self):
        result = judge(BOOK, PROBLEM, "python", "def broken(:\n    pass\n")
        self.assertEqual(result["status"], "Compile Error")

    def test_runtime_error(self):
        result = judge(BOOK, PROBLEM, "python", "raise RuntimeError('T001')\n")
        self.assertEqual(result["status"], "Runtime Error")
        self.assertEqual(result["case"], 1)

    def test_time_limit_is_enforced(self):
        result = judge(BOOK, PROBLEM, "python", "while True:\n    pass\n")
        self.assertEqual(result["status"], "Time Limit Exceeded")

    def test_output_limit_is_enforced(self):
        source = "print('x' * (2 * 1024 * 1024 + 1))\n"
        result = judge(BOOK, PROBLEM, "python", source)
        self.assertEqual(result["status"], "Output Limit Exceeded")


if __name__ == "__main__":
    unittest.main()
