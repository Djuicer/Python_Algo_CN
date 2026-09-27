"""
首个已知超过一百万位的素数发现于 1999 年，是形如 2**6972593 - 1 的 Mersenne 素数；
它恰好包含 2,098,960 位。随后又发现了其他形如 2**p - 1、位数更多的 Mersenne 素数。
然而，2004 年发现了一个包含 2,357,207 位的巨大非 Mersenne 素数：
(28433 * (2 ** 7830457 + 1))。

求该素数的最后十位数字。
"""


def solution(n: int = 10) -> str:
    """
    返回 NUMBER 的最后 n 位数字。
    >>> solution()
    '8739992577'
    >>> solution(8)
    '39992577'
    >>> solution(1)
    '7'
    >>> solution(-1)
    Traceback (most recent call last):
        ...
    ValueError: Invalid input
    >>> solution(8.3)
    Traceback (most recent call last):
        ...
    ValueError: Invalid input
    >>> solution("a")
    Traceback (most recent call last):
        ...
    ValueError: Invalid input
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Invalid input")
    modulus = 10**n
    number = 28433 * (pow(2, 7830457, modulus)) + 1
    return str(number % modulus)


if __name__ == "__main__":
    from doctest import testmod

    testmod()
    print(f"{solution(10) = }")
