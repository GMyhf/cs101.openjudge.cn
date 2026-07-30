"""Exact-answer validators shared by GMyhf materialization and full-sweep gates."""
from itertools import product


def is_subsequence(candidate, text):
    offset = 0
    for character in candidate:
        offset = text.find(character, offset)
        if offset < 0:
            return False
        offset += 1
    return True


def divisible_by_eight_answers(text):
    """All legal one-to-three digit output strings for CF 550C / problem 27150."""
    alphabet = sorted(set(text.strip()))
    answers = set()
    for length in (1, 2, 3):
        for digits in product(alphabet, repeat=length):
            candidate = "".join(digits)
            if int(candidate) % 8 == 0 and is_subsequence(candidate, text):
                answers.add(candidate)
    return answers


def longer_answer_witness(text):
    """找一个**比三位更长**、同样合法的输出，找不到返回 None。

    为什么非要有这一步：合法输出**不限长度**，而 `divisible_by_eight_answers()` 只枚举
    1..3 位。能被 8 整除只由**最后三位**决定 —— 所以只要存在一个三位答案 `c`，
    在 `c` 最早那次嵌入之前还有任何一个非零数字 `d`，那么 `d + c` 就是又一个合法输出
    （四位以上，末三位仍是 `c`）。**这不是理论顾虑**：2026-07-30 复核实测，
    27150 保留的 19 组里有 5 组正是这样 —— 期望 `992`，而 `9992` 同样合法；
    期望 `112`，而 `1112`/`2112` 同样合法。只按 1..3 位判"唯一"会给一份
    **实际上会误杀正确解法**的数据发通行证。

    只对三位答案成立：往两位或一位答案前面加数字会改变整数值，不保证还能被 8 整除。

    判法：取**第一个非零数字** `d`（位置 q），若三位答案 `c` 在 `text[q+1:]` 里仍是子序列，
    则 `d + c` 合法。注意不能反过来查「`c` 最早嵌入之前有没有非零数字」——
    `c` 往往就是从第 0 位开始嵌入的，那样永远找不到证人，而真正的构造是
    **把 `c` 换成靠后的那次嵌入**，再拿前面的数字打头。
    """
    stripped = text.strip()
    position = next((index for index, digit in enumerate(stripped) if digit != "0"), None)
    if position is None:
        return None
    tail = stripped[position + 1:]
    for candidate in sorted(divisible_by_eight_answers(text)):
        if len(candidate) == 3 and is_subsequence(candidate, tail):
            return stripped[position] + candidate
    return None


def analyze_27150_case(input_text, output_text):
    answers = divisible_by_eight_answers(input_text)
    tokens = output_text.split()
    expected = tokens[1] if len(tokens) == 2 and tokens[0] == "YES" else None
    witness = longer_answer_witness(input_text) if answers else None
    valid_unique = ((not answers and tokens == ["NO"]) or
                    (len(answers) == 1 and expected in answers and witness is None))
    return {"valid_unique": valid_unique, "answers": answers,
            "longer_answer": witness,
            "kind": "YES" if answers else "NO"}
