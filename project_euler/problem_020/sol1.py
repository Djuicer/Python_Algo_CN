"""
Problem 20: https://projecteuler.net/problem=20

n! 表示 n x (n - 1) x ... x 3 x 2 x 1

例如，10! = 10 x 9 x ... x 3 x 2 x 1 = 3628800，
数 10! 的各位数字之和为 3 + 6 + 2 + 8 + 8 + 0 + 0 = 27。

求数 100! 的各位数字之和。
"""


def factorial(num: int) -> int:
    """计算给定数字 n 的阶乘。"""
    fact = 1
    for i in range(1, num + 1):
        fact *= i
    return fact


def split_and_add(number: int) -> int:
    """拆分数字的各位并求和。"""
    sum_of_digits = 0
    while number > 0:
        last_digit = number % 10
        sum_of_digits += last_digit
        number = number // 10  # 从给定数字中移除 last_digit
    return sum_of_digits


def solution(num: int = 100) -> int:
    """返回 num 的阶乘的各位数字之和。
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
    """
    nfact = factorial(num)
    result = split_and_add(nfact)
    return result


if __name__ == "__main__":
    print(solution(int(input("Enter the Number: ").strip())))
