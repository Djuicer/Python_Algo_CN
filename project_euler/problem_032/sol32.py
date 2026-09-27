"""
如果一个 n 位数恰好使用了 1 到 n 的每个数字一次，就称其为全数字数；
例如，5 位数 15234 是由 1 到 5 构成的全数字数。

乘积 7254 很特别，因为等式 39 x 186 = 7254 中的被乘数、乘数和乘积合起来
是由 1 到 9 构成的全数字数。

求所有满足“被乘数/乘数/乘积”恒等式可写成 1 到 9 全数字形式的乘积之和。

提示：某些乘积可由多种方式得到，因此求和时务必只计入一次。
"""

import itertools


def is_combination_valid(combination):
    """
    检查一个组合（由 9 个数字组成的元组）是否为有效的乘积等式。

    >>> is_combination_valid(('3', '9', '1', '8', '6', '7', '2', '5', '4'))
    True

    >>> is_combination_valid(('1', '2', '3', '4', '5', '6', '7', '8', '9'))
    False

    """
    return (
        int("".join(combination[0:2])) * int("".join(combination[2:5]))
        == int("".join(combination[5:9]))
    ) or (
        int("".join(combination[0])) * int("".join(combination[1:5]))
        == int("".join(combination[5:9]))
    )


def solution():
    """
    求所有满足“被乘数/乘数/乘积”恒等式可写成 1 到 9 全数字形式的乘积之和。

    >>> solution()
    45228
    """

    return sum(
        {
            int("".join(pandigital[5:9]))
            for pandigital in itertools.permutations("123456789")
            if is_combination_valid(pandigital)
        }
    )


if __name__ == "__main__":
    print(solution())
