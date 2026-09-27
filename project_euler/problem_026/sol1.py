"""
Euler Problem 26
https://projecteuler.net/problem=26

题目说明：

单位分数的分子为 1。分母从 2 到 10 的单位分数，其十进制表示如下：

1/2	= 	0.5
1/3	= 	0.(3)
1/4	= 	0.25
1/5	= 	0.2
1/6	= 	0.1(6)
1/7	= 	0.(142857)
1/8	= 	0.125
1/9	= 	0.(1)
1/10	= 	0.1
其中 0.1(6) 表示 0.166666...，其循环节为 1 位。可以看出，1/7 的循环节为 6 位。

求满足 d < 1000 且 1/d 的小数部分具有最长循环节的 d 值。
"""


def solution(numerator: int = 1, digit: int = 1000) -> int:
    """
    可以提供任意范围；题目要求数字 d < 1000。
    >>> solution(1, 10)
    7
    >>> solution(10, 100)
    97
    >>> solution(10, 1000)
    983
    """
    the_digit = 1
    longest_list_length = 0

    for divide_by_number in range(numerator, digit + 1):
        has_been_divided: list[int] = []
        now_divide = numerator
        for _ in range(1, digit + 1):
            if now_divide in has_been_divided:
                if longest_list_length < len(has_been_divided):
                    longest_list_length = len(has_been_divided)
                    the_digit = divide_by_number
            else:
                has_been_divided.append(now_divide)
                now_divide = now_divide * 10 % divide_by_number

    return the_digit


# 测试
if __name__ == "__main__":
    import doctest

    doctest.testmod()
