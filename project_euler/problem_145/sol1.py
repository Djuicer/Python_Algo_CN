"""
Project Euler problem 145: https://projecteuler.net/problem=145
Author: Vineet Rao, Maxim Smolskiy
题目说明：

某些正整数 n 具有如下性质：和 [ n + reverse(n) ] 的所有十进制数字均为奇数。
例如，36 + 63 = 99 且 409 + 904 = 1313。
称这样的数为可逆数；因此 36, 63, 409, and 904 都是可逆数。
n 和 reverse(n) 都不允许有前导零。

一千以下共有 120 个可逆数。

十亿 (10^9) 以下有多少个可逆数？
"""

EVEN_DIGITS = [0, 2, 4, 6, 8]
ODD_DIGITS = [1, 3, 5, 7, 9]


def slow_reversible_numbers(
    remaining_length: int, remainder: int, digits: list[int], length: int
) -> int:
    """
    计算给定长度的可逆数数量。
    根据当前和的余数奇偶性遍历可能的数字。
    >>> slow_reversible_numbers(1, 0, [0], 1)
    0
    >>> slow_reversible_numbers(2, 0, [0] * 2, 2)
    20
    >>> slow_reversible_numbers(3, 0, [0] * 3, 3)
    100
    """
    if remaining_length == 0:
        if digits[0] == 0 or digits[-1] == 0:
            return 0

        for i in range(length // 2 - 1, -1, -1):
            remainder += digits[i] + digits[length - i - 1]

            if remainder % 2 == 0:
                return 0

            remainder //= 10

        return 1

    if remaining_length == 1:
        if remainder % 2 == 0:
            return 0

        result = 0
        for digit in range(10):
            digits[length // 2] = digit
            result += slow_reversible_numbers(
                0, (remainder + 2 * digit) // 10, digits, length
            )
        return result

    result = 0
    for digit1 in range(10):
        digits[(length + remaining_length) // 2 - 1] = digit1

        if (remainder + digit1) % 2 == 0:
            other_parity_digits = ODD_DIGITS
        else:
            other_parity_digits = EVEN_DIGITS

        for digit2 in other_parity_digits:
            digits[(length - remaining_length) // 2] = digit2
            result += slow_reversible_numbers(
                remaining_length - 2,
                (remainder + digit1 + digit2) // 10,
                digits,
                length,
            )
    return result


def slow_solution(max_power: int = 9) -> int:
    """
    要计算问题答案，请使用 solution()。
    >>> slow_solution(3)
    120
    >>> slow_solution(6)
    18720
    >>> slow_solution(7)
    68720
    """
    result = 0
    for length in range(1, max_power + 1):
        result += slow_reversible_numbers(length, 0, [0] * length, length)
    return result


def reversible_numbers(
    remaining_length: int, remainder: int, digits: list[int], length: int
) -> int:
    """
    计算给定长度的可逆数数量。
    根据当前和的余数奇偶性遍历可能的数字。
    >>> reversible_numbers(1, 0, [0], 1)
    0
    >>> reversible_numbers(2, 0, [0] * 2, 2)
    20
    >>> reversible_numbers(3, 0, [0] * 3, 3)
    100
    """
    # 不存在 1, 5, 9, 13 (ie. 4k+1) 位的可逆数
    if (length - 1) % 4 == 0:
        return 0

    return slow_reversible_numbers(remaining_length, remainder, digits, length)


def solution(max_power: int = 9) -> int:
    """
    要计算问题答案，请使用 solution()。
    >>> solution(3)
    120
    >>> solution(6)
    18720
    >>> solution(7)
    68720
    """
    result = 0
    for length in range(1, max_power + 1):
        result += reversible_numbers(length, 0, [0] * length, length)
    return result


def benchmark() -> None:
    """
    基准测试
    """
    # 运行性能基准测试……
    # slow_solution : 292.9300301000003
    # solution      : 54.90970860000016

    from timeit import timeit

    print("Running performance benchmarks...")

    print(f"slow_solution : {timeit('slow_solution()', globals=globals(), number=10)}")
    print(f"solution      : {timeit('solution()', globals=globals(), number=10)}")


if __name__ == "__main__":
    print(f"Solution : {solution()}")
    benchmark()

    # for i in range(1, 15):
    #     print(f"{i}. {reversible_numbers(i, 0, [0]*i, i)}")
