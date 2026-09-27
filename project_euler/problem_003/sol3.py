"""
Project Euler Problem 3: https://projecteuler.net/problem=3

最大质因数

13195 的质因数为 5、7、13 和 29。

数 600851475143 的最大质因数是多少？

参考资料：
    - https://en.wikipedia.org/wiki/Prime_number#Unique_factorization
"""


def solution(n: int = 600851475143) -> int:
    """
    返回给定数 n 的最大质因数。

    >>> solution(13195)
    29
    >>> solution(10)
    5
    >>> solution(17)
    17
    >>> solution(3.4)
    3
    >>> solution(0)
    Traceback (most recent call last):
        ...
    ValueError: Parameter n must be greater than or equal to one.
    >>> solution(-17)
    Traceback (most recent call last):
        ...
    ValueError: Parameter n must be greater than or equal to one.
    >>> solution([])
    Traceback (most recent call last):
        ...
    TypeError: Parameter n must be int or castable to int.
    >>> solution("asd")
    Traceback (most recent call last):
        ...
    TypeError: Parameter n must be int or castable to int.
    """

    try:
        n = int(n)
    except TypeError, ValueError:
        raise TypeError("Parameter n must be int or castable to int.")
    if n <= 0:
        raise ValueError("Parameter n must be greater than or equal to one.")
    i = 2
    ans = 0
    if n == 2:
        return 2
    while n > 2:
        while n % i != 0:
            i += 1
        ans = i
        while n % i == 0:
            n = n // i
        i += 1
    return int(ans)


if __name__ == "__main__":
    print(f"{solution() = }")
