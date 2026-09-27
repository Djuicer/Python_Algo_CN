"""
Project Euler Problem 80: https://projecteuler.net/problem=80
Author: Sandeep Gupta
题目说明：对于前一百个自然数，求所有无理平方根小数部分前一百位数字之和的总和。
Time: 5 October 2020, 18:30
"""

import decimal


def solution() -> int:
    """
    为计算该总和，使用 Python 的 decimal 模块计算到小数点后 100 位。
    最重要的是额外计算几位小数，否则会产生舍入误差。

    >>> solution()
    40886
    """
    answer = 0
    decimal_context = decimal.Context(prec=105)
    for i in range(2, 100):
        number = decimal.Decimal(i)
        sqrt_number = number.sqrt(decimal_context)
        if len(str(sqrt_number)) > 1:
            answer += int(str(sqrt_number)[0])
            sqrt_number_str = str(sqrt_number)[2:101]
            answer += sum(int(x) for x in sqrt_number_str)
    return answer


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(f"{solution() = }")
