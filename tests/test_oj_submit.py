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

    def test_poll_asks_the_group_url_not_a_hardcoded_practice_url(self):
        """上面那条把 `poll` 整个 mock 掉了，所以它只钉住了「参数传下去了」。

        401 那个 bug 的真身在 `poll` **内部拼 URL** 那一行。把 `poll` mock 掉之后，
        那一行改回写死 `/practice/` 照样全绿 —— 实测过。所以这里不 mock `poll`，
        只 mock 它底下的 `_get`，直接看它请求的是哪个地址。
        """
        session = oj_submit.Session()
        asked = []

        def fake_get(url):
            asked.append(url)
            return "<html>Accepted 12ms</html>"

        with mock.patch.object(session, "_get", side_effect=fake_get):
            result = session.poll("42", group="2024fallroutine")

        self.assertEqual(result["verdict"], "Accepted")
        self.assertTrue(asked, "poll 一次都没发请求")
        self.assertIn("/2024fallroutine/solution/42/", asked[0])
        self.assertNotIn("/practice/", asked[0])


if __name__ == "__main__":
    unittest.main()
