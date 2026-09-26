"""
组合总和（Combination Sum）问题给定一个由互不相同的整数组成的列表，
要求找出所有元素和等于给定目标值的组合。
每个元素可以使用多次。

时间复杂度（平均情况）：O(n!)

约束：
1 <= candidates.length <= 30
2 <= candidates[i] <= 40
candidates 中所有元素互不相同。
1 <= target <= 40
"""


def backtrack(
    candidates: list, path: list, answer: list, target: int, previous_index: int
) -> None:
    """
    递归搜索可能的组合。当当前组合的元素和
    大于目标值时回溯。

    Parameters
    ----------
    previous_index: 上一次搜索的最后一个索引
    target: path 列表中的整数相加需要得到的值。
    answer: 可能的组合列表
    path: 当前组合
    candidates: 可以使用的整数列表。
    """
    if target == 0:
        answer.append(path.copy())
    else:
        for index in range(previous_index, len(candidates)):
            if target >= candidates[index]:
                path.append(candidates[index])
                backtrack(candidates, path, answer, target - candidates[index], index)
                path.pop(len(path) - 1)


def combination_sum(candidates: list, target: int) -> list:
    """
    >>> combination_sum([2, 3, 5], 8)
    [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    >>> combination_sum([2, 3, 6, 7], 7)
    [[2, 2, 3], [7]]
    >>> combination_sum([-8, 2.3, 0], 1)
    Traceback (most recent call last):
        ...
    ValueError: All elements in candidates must be non-negative
    >>> combination_sum([], 1)
    Traceback (most recent call last):
        ...
    ValueError: Candidates list should not be empty
    """
    if not candidates:
        raise ValueError("Candidates list should not be empty")

    if any(x < 0 for x in candidates):
        raise ValueError("All elements in candidates must be non-negative")

    path = []  # type: list[int]
    answer = []  # type: list[int]
    backtrack(candidates, path, answer, target, 0)
    return answer


def main() -> None:
    print(combination_sum([-8, 2.3, 0], 1))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    main()
