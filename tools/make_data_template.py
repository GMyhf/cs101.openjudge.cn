#!/usr/bin/env python3
"""测试数据生成器模版 · <book>/<problem_id> <题目标题>

用法：为一道缺测试数据的题目复制本文件为
  data/openjudge/tests/<bucket>/<全局题号>_made/make_data.py
由 LLM 按题面填写 solve() / gen_cases() / SAMPLES，然后在该目录下执行：
  python3 make_data.py
通过自检后生成 01.in/01.out、02.in/02.out …，`scripts/index_tests.py` 会自动索引
（目录名里的数字就是题号，`_made` 后缀标记「生成数据」的出处）。

硬规则：
- SAMPLES 必须从题面**原样**复制，一字不改；自检强制 solve() 复现所有样例。
- gen_cases() 第一组放题面样例，然后是边界（最小/最大规模），最后是随机；
  随机必须用固定种子，保证可复现。
- 规模守住判题限制：单组 CPU 4 秒、输出 ≤ 2 MiB。
- 若题目接受多种正确输出（构造题/任意解/浮点误差），本地判题是 token 精确比对，
  **不要生成**——在批次报告里把题号列入「需 special judge」清单。
"""
import random
from pathlib import Path

SEED = 0  # 改成题号，固定可复现


def solve(input_text: str) -> str:
    """参考解法：接收整个 stdin 文本，返回整个 stdout 文本。

    这是数据正确性的唯一来源，必须先通过题面样例（下方自检强制）。
    优先写最朴素、最不可能写错的解法；效率只要在 4 秒内跑完自己生成的数据即可。
    """
    raise NotImplementedError


def gen_cases() -> list[str]:
    """返回每组测试的 .in 文本（含结尾换行）。

    覆盖顺序：题面样例 → 边界（最小 N、最大 N、全同值、退化形状…）→ 固定种子随机。
    一般 5-10 组足够。
    """
    rng = random.Random(SEED)
    cases = [SAMPLES[0][0]]
    # ... 边界与随机组 ...
    return cases


# 从题面原样复制，一字不改（可多组）
SAMPLES = [
    ("<样例输入>\n", "<样例输出>\n"),
]


def main():
    for index, (sample_in, sample_out) in enumerate(SAMPLES, 1):
        got = solve(sample_in)
        assert got.split() == sample_out.split(), (
            f"样例 {index} 不匹配：参考解法输出 {got!r}，题面给的是 {sample_out!r}"
        )
    here = Path(__file__).parent
    cases = gen_cases()
    for index, case_in in enumerate(cases, 1):
        (here / f"{index:02d}.in").write_text(case_in, encoding="utf-8")
        (here / f"{index:02d}.out").write_text(solve(case_in), encoding="utf-8")
    print(f"ok: {len(cases)} cases, samples verified")


if __name__ == "__main__":
    main()
