"""
Project Euler Problem 800: https://projecteuler.net/problem=800

形如 p^q q^p，其中质数 p != q 的整数称为混合整数。
例如，800 = 2^5 5^2 是一个混合整数。

定义 C(n) 为小于或等于 n 的混合整数的数量。
已知 C(800) = 2 且 C(800^800) = 10790

求 C(800800^800800)
"""

from math import isqrt, log2


def calculate_prime_numbers(max_number: int) -> list[int]:
    """
    返回小于 max_number 的质数。

    >>> calculate_prime_numbers(10)
    [2, 3, 5, 7]
    """

    is_prime = [True] * max_number
    for i in range(2, isqrt(max_number - 1) + 1):
        if is_prime[i]:
            for j in range(i**2, max_number, i):
                is_prime[j] = False

    return [i for i in range(2, max_number) if is_prime[i]]


def solution(base: int = 800800, degree: int = 800800) -> int:
    """
    返回小于或等于 base^degree 的混合整数数量。

    >>> solution(800, 1)
    2

    >>> solution(800, 800)
    10790
    """

    upper_bound = degree * log2(base)
    max_prime = int(upper_bound)
    prime_numbers = calculate_prime_numbers(max_prime)

    hybrid_integers_count = 0
    left = 0
    right = len(prime_numbers) - 1
    while left < right:
        while (
            prime_numbers[right] * log2(prime_numbers[left])
            + prime_numbers[left] * log2(prime_numbers[right])
            > upper_bound
        ):
            right -= 1
        hybrid_integers_count += right - left
        left += 1

    return hybrid_integers_count


if __name__ == "__main__":
    print(f"{solution() = }")
