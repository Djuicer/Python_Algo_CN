"""
Problem 20: https://projecteuler.net/problem=20

n! 表示 n x (n - 1) x ... x 3 x 2 x 1

例如，10! = 10 x 9 x ... x 3 x 2 x 1 = 3628800，
数 10! 的各位数字之和为 3 + 6 + 2 + 8 + 8 + 0 + 0 = 27。

求数 100! 的各位数字之和。
"""

from math import factorial


def solution(num: int = 100) -> int:
    """返回 num 的阶乘的各位数字之和。
    >>> solution(1000)
    10539
    >>> solution(200)
    1404
    >>> solution(100)
    648
    >>> solution(50)
    216
    >>> solution(10)
    27
    >>> solution(5)
    3
    >>> solution(3)
    6
    >>> solution(2)
    2
    >>> solution(1)
    1
    >>> solution(0)
    1
    """
    return sum(map(int, str(factorial(num))))


if __name__ == "__main__":
    print(solution(int(input("Enter the Number: ").strip())))
