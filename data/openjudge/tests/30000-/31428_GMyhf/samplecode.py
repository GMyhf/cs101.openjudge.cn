def two_sum(nums: list[int], target: int) -> tuple[int, int]:
    seen = {}
    for index, value in enumerate(nums):
        if target - value in seen:
            return seen[target - value], index
        seen[value] = index
    raise ValueError("No solution")
