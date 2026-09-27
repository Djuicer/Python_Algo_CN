#!/usr/bin/env python3


def climb_stairs(number_of_steps: int) -> int:
    """
    LeetCdoe 第 70 题：爬楼梯
    爬上具有 number_of_steps 级台阶的楼梯，每次可以爬 1 级或 2 级，
    计算不同的爬法数量。

    参数：
        number_of_steps: 楼梯的台阶数

    返回：
        爬上具有 number_of_steps 级台阶的楼梯的不同方式数

    异常：
        AssertionError: number_of_steps 不是正整数

    >>> climb_stairs(3)
    3
    >>> climb_stairs(1)
    1
    >>> climb_stairs(-7)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    AssertionError: number_of_steps needs to be positive integer, your input -7
    """
    assert isinstance(number_of_steps, int) and number_of_steps > 0, (
        f"number_of_steps needs to be positive integer, your input {number_of_steps}"
    )
    if number_of_steps == 1:
        return 1
    previous, current = 1, 1
    for _ in range(number_of_steps - 1):
        current, previous = current + previous, current
    return current


if __name__ == "__main__":
    import doctest

    doctest.testmod()
