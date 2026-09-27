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
    prime = 1
    i = 2
    while i * i <= n:
        while n % i == 0:
            prime = i
            n //= i
        i += 1
    if n > 1:
        prime = n
    return int(prime)


if __name__ == "__main__":
    print(f"{solution() = }")
