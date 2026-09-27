"""
Project Euler Problem 2: https://projecteuler.net/problem=2

偶数斐波那契数

斐波那契数列中的每个新项都由前两项相加得到。从 1 和 2 开始，前 10 项为：

1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...

考虑斐波那契数列中值不超过四百万的项，求其中偶数项之和。

参考资料：
    - https://en.wikipedia.org/wiki/Fibonacci_number
"""


def solution(n: int = 4000000) -> int:
    """
    返回斐波那契数列中所有小于或等于 n 的偶数项之和。

    >>> solution(10)
    10
    >>> solution(15)
    10
    >>> solution(2)
    2
    >>> solution(1)
    0
    >>> solution(34)
    44
    """

    if n <= 1:
        return 0
    a = 0
    b = 2
    count = 0
    while 4 * b + a <= n:
        a, b = b, 4 * b + a
        count += a
    return count + b


if __name__ == "__main__":
    print(f"{solution() = }")
