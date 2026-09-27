"""
Project Euler Problem 074: https://projecteuler.net/problem=74

数 145 因其各位数字的阶乘之和等于 145 而广为人知：

1! + 4! + 5! = 1 + 24 + 120 = 145

可能较少有人知道，169 会产生回到 169 的最长数字链；事实证明仅存在以下三个循环：

169 → 363601 → 1454 → 169
871 → 45361 → 871
872 → 45362 → 872

不难证明，每个起始数最终都会陷入循环。例如：

69 → 363600 → 1454 → 169 → 363601 (→ 1454)
78 → 45360 → 871 → 45361 (→ 871)
540 → 145 (→ 145)

从 69 开始会产生包含五个不重复项的链，而起始数低于一百万的最长不重复链包含六十项。

起始数低于一百万且恰好包含六十个不重复项的链有多少条？

解法思路：
本解法使用一个循环，利用先前链的缓存长度生成不重复项链。
遇到重复项之前，或链长度大于目标长度时停止生成。
每条链生成后检查其长度，并增加计数器。
"""

from math import factorial

DIGIT_FACTORIAL: dict[str, int] = {str(digit): factorial(digit) for digit in range(10)}


def digit_factorial_sum(number: int) -> int:
    """
    计算 number 的各位数字阶乘之和。

    >>> digit_factorial_sum(69.0)
    Traceback (most recent call last):
        ...
    TypeError: Parameter number must be int

    >>> digit_factorial_sum(-1)
    Traceback (most recent call last):
        ...
    ValueError: Parameter number must be greater than or equal to 0

    >>> digit_factorial_sum(0)
    1

    >>> digit_factorial_sum(69)
    363600
    """
    if not isinstance(number, int):
        raise TypeError("Parameter number must be int")

    if number < 0:
        raise ValueError("Parameter number must be greater than or equal to 0")

    # Converts number in string to iterate on its digits and adds its factorial.
    return sum(DIGIT_FACTORIAL[digit] for digit in str(number))


def solution(chain_length: int = 60, number_limit: int = 1000000) -> int:
    """
    返回 number_limit 以下能产生恰含 chain_length 个不重复元素之链的数字数量。

    >>> solution(10.0, 1000)
    Traceback (most recent call last):
        ...
    TypeError: Parameters chain_length and number_limit must be int

    >>> solution(10, 1000.0)
    Traceback (most recent call last):
        ...
    TypeError: Parameters chain_length and number_limit must be int

    >>> solution(0, 1000)
    Traceback (most recent call last):
        ...
    ValueError: Parameters chain_length and number_limit must be greater than 0

    >>> solution(10, 0)
    Traceback (most recent call last):
        ...
    ValueError: Parameters chain_length and number_limit must be greater than 0

    >>> solution(10, 1000)
    26
    """

    if not isinstance(chain_length, int) or not isinstance(number_limit, int):
        raise TypeError("Parameters chain_length and number_limit must be int")

    if chain_length <= 0 or number_limit <= 0:
        raise ValueError(
            "Parameters chain_length and number_limit must be greater than 0"
        )

    # the counter for the chains with the exact desired length
    chains_counter = 0
    # the cached sizes of the previous chains
    chain_sets_lengths: dict[int, int] = {}

    for start_chain_element in range(1, number_limit):
        # The temporary set will contain the elements of the chain
        chain_set = set()
        chain_set_length = 0

        # Stop computing the chain when you find a cached size, a repeating item or the
        # length is greater then the desired one.
        chain_element = start_chain_element
        while (
            chain_element not in chain_sets_lengths
            and chain_element not in chain_set
            and chain_set_length <= chain_length
        ):
            chain_set.add(chain_element)
            chain_set_length += 1
            chain_element = digit_factorial_sum(chain_element)

        if chain_element in chain_sets_lengths:
            chain_set_length += chain_sets_lengths[chain_element]

        chain_sets_lengths[start_chain_element] = chain_set_length

        # If chain contains the exact amount of elements increase the counter
        if chain_set_length == chain_length:
            chains_counter += 1

    return chains_counter


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(f"{solution()}")
