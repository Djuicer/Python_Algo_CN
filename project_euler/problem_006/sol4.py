"""
Project Euler Problem 6: https://projecteuler.net/problem=6

平方和之差

前十个自然数的平方和为：
    1^2 + 2^2 + ... + 10^2 = 385

前十个自然数之和的平方为：
    (1 + 2 + ... + 10)^2 = 55^2 = 3025

因此，前十个自然数的平方和与其和的平方之差为 3025 - 385 = 2640。

求前一百个自然数的平方和与其和的平方之差。
"""


def solution(n: int = 100) -> int:
    """
    返回前 n 个自然数的平方和与其和的平方之差。

    >>> solution(10)
    2640
    >>> solution(15)
    13160
    >>> solution(20)
    41230
    >>> solution(50)
    1582700
    """

    sum_of_squares = n * (n + 1) * (2 * n + 1) / 6
    square_of_sum = (n * (n + 1) / 2) ** 2
    return int(square_of_sum - sum_of_squares)


if __name__ == "__main__":
    print(f"{solution() = }")
