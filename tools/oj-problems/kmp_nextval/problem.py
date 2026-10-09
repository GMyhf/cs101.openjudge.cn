"""私有题 1000000「KMP 字符比较次数（nextval）」的 oj-problem-tools 版本，用来上传到 cs101.openjudge.cn。

运行（在 cs101 仓库根目录）：

    uv run --project ../oj-problem-tools tools/oj-problems/kmp_nextval/problem.py

**数据与本站逐字节相同**：输入直接调用本站生成器
`data/openjudge/tests/private/1000000_made/producecase.py`（第 0 组是题面样例，
第 i 组 = `generate(1000000, i)`），不用框架传进来的 `random` —— 两边各造一份就会出现
「本站判对、平台判错」的两套数据。答案用 `tests/test_private_1000000.py` 里那份独立 oracle
（暴力求 border / Z 函数），与 `solution.py`（即本站参考实现）算法不同，框架的对拍才有意义。

自动更新平台题面：人先在平台建好占位题，再把下面两行的注释去掉、填上题号。
"""
import shutil
import sys
from pathlib import Path
from random import Random

from oj_problem_tools import OjProblem

REPO = Path(__file__).resolve().parents[3]
MADE = REPO / "data/openjudge/tests/private/1000000_made"
for path in (REPO, MADE, REPO / "tests"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import producecase  # noqa: E402
from test_private_1000000 import oracle  # noqa: E402


class KmpNextval(OjProblem[str, str]):
    case_range = range(producecase.TOTAL)
    interpreter = shutil.which("python3.8") or sys.executable
    # group_slug = "cs101"
    # problem_id = 0

    def generate(self, index: int, random: Random) -> str:
        if index < len(producecase.SAMPLES):
            return producecase.SAMPLES[index][0]
        return producecase.generate(producecase.NUMBER, index)

    def solve(self, data: str, index: int) -> str | None:
        if producecase.valid(data) is not True:
            raise ValueError(f"第 {index} 组违反输入契约：{producecase.valid(data)}")
        answer = oracle(data)
        if index < len(producecase.SAMPLES) and answer != producecase.SAMPLES[index][1]:
            raise ValueError(f"第 {index} 组与题面样例输出不符：{answer!r}")
        return answer


if __name__ == "__main__":
    # 与框架的 `_auto_run` 同一流程，只多一条：无图形界面的服务器上没有剪贴板，
    # `pyperclip.copy` 会抛异常把后面的生成与对拍一起打断 —— inject.js 此时已经写好了。
    # 显式实例化后框架就不再在退出时自动跑一遍。
    import pyperclip

    problem = KmpNextval()
    if problem.group_slug and problem.problem_id:
        problem.update_problem()
    else:
        try:
            problem.generate_inject_script()
        except pyperclip.PyperclipException:
            print(f"没有剪贴板，inject.js 已写到 {problem.inject_js_output}，请手动打开复制。")
    problem.generate_all()
    problem.test_solution()
