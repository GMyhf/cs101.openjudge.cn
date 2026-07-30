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


def analyze_27150_case(input_text, output_text):
    answers = divisible_by_eight_answers(input_text)
    tokens = output_text.split()
    expected = tokens[1] if len(tokens) == 2 and tokens[0] == "YES" else None
    valid_unique = ((not answers and tokens == ["NO"]) or
                    (len(answers) == 1 and expected in answers))
    return {"valid_unique": valid_unique, "answers": answers,
            "kind": "YES" if answers else "NO"}
