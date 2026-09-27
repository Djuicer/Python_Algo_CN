"""
Project Euler Problem 10: https://projecteuler.net/problem=10

质数求和

小于 10 的质数之和为 2 + 3 + 5 + 7 = 17。

求所有小于两百万的质数之和。

参考资料：
    - https://en.wikipedia.org/wiki/Prime_number
    - https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
"""


def solution(n: int = 2000000) -> int:
    """
    使用埃拉托斯特尼筛法（Sieve of Eratosthenes）返回所有小于 n 的质数之和：

    当 n 小于 1000 万时，埃拉托斯特尼筛法是查找所有小于 n 的质数的
    高效方法之一。仅适用于正数。

    >>> solution(1000)
    76127
    >>> solution(5000)
    1548136
    >>> solution(10000)
    5736396
    >>> solution(7)
    10
    >>> solution(7.1)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: 'float' object cannot be interpreted as an integer
    >>> solution(-7)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    IndexError: list assignment index out of range
    >>> solution("seven")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: can only concatenate str (not "int") to str
    """

    primality_list = [0 for i in range(n + 1)]
    primality_list[0] = 1
    primality_list[1] = 1

    for i in range(2, int(n**0.5) + 1):
        if primality_list[i] == 0:
            for j in range(i * i, n + 1, i):
                primality_list[j] = 1
    sum_of_primes = 0
    for i in range(n):
        if primality_list[i] == 0:
            sum_of_primes += i
    return sum_of_primes


if __name__ == "__main__":
    print(f"{solution() = }")
