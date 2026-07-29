"""Regression tests for the OpenJudge platform submission helper."""
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import oj_submit


class SubmitSessionTests(unittest.TestCase):
    def test_run_polls_the_group_used_for_submission(self):
        session = oj_submit.Session()
        with mock.patch.object(session, "submit", return_value="42") as submit:
            with mock.patch.object(session, "poll", return_value={"verdict": "Accepted"}) as poll:
                result = session.run("02707", "print(1)", "Python3", "routine")

        self.assertEqual(result["verdict"], "Accepted")
        submit.assert_called_once_with("02707", "print(1)", "Python3", "routine")
        poll.assert_called_once_with("42", group="routine")


if __name__ == "__main__":
    unittest.main()
