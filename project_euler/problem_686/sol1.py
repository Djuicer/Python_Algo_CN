"""
Project Euler Problem 686: https://projecteuler.net/problem=686

2^7 = 128 是首位数字为 "12" 的第一个 2 的幂。
首位数字为 "12" 的下一个 2 的幂是 2^80。

定义 p(L,n) 为第 n 小的 j 值，使得 2^j 的十进制表示以 L 的各位数字开头。

因此 p(12, 1) = 7，且 p(12, 2) = 80。

已知 p(123, 45) = 12710。

求 p(123, 678910)。
"""

import math


def log_difference(number: int) -> float:
    """
    此函数返回一个数乘以 log(2) 后的小数部分。
    由于本题涉及 2 的幂，计算指数很大的 2 的幂非常耗时。
    因此使用 log 来减少计算时间。

    可以发现，首位数字为 123 的第一个 2 的幂指数是 90。
    计算 2^90 非常耗时。
    因此计算 log(2^90) = 90*log(2) = 27.092699609758302
    但要判断该幂是否以 123 开头，只需要小数部分。
    所以只返回对数乘积的小数部分。
    因此返回 0.092699609758302

    >>> log_difference(90)
    0.092699609758302
    >>> log_difference(379)
    0.090368356648852

    """

    log_number = math.log(2, 10) * number
    difference = round((log_number - int(log_number)), 15)

    return difference


def solution(number: int = 678910) -> int:
    """
    此函数计算第 n 个（n = number）满足 2^power 的首位数字为 123 的
    最小 2 的幂指数 power。

    例如，首位数字为 123 的 2 的幂指数依次为：
    90, 379, 575, 864, 1060, 1545, 1741, 2030, 2226, 2515，依此类推。
    90 是首位数字为 123 的第一个 2 的幂指数，
    379 是首位数字为 123 的第二个 2 的幂指数，依此类推。

    因此，如果 number = 10，根据上述数列，solution 返回 2515。

    定义一个下界和一个上界。
    lowerbound = log(1.23), upperbound = log(1.24)
    因为需要找到首位数字为 123 的幂。

    log(1.23) = 0.08990511143939792, log(1,24) = 0.09342168516223506.
    使用 1.23 而不是 12.3 或 123，是因为 log(1.23) 只产生小于 1 的小数值。
    log(12.3) 的小数部分相同，但会加上 1，
    即 log(12.3) = 1.093421685162235。
    可以看到，无论是 1.23 还是 12.3，小数部分都保持不变。
    由于函数 log_difference() 只返回小数部分，因此使用 1.23 是合理的。

    可以看到，90*log(2) = 27.092699609758302，
    小数部分 = 0.092699609758302，位于下界和上界之间。

    首位数字为 123 的各个幂指数之间的差如下：

    379 - 90 = 289
    575 - 379 = 196
    864 - 575 = 289
    1060 - 864 = 196

    可以发现一个规律：差值要么是 196，要么是 289 = 196 + 93。

    因此，为了优化算法，将根据 log_difference() 的值增加 196 或 93。

    以 90 为例。
    由于 90 是首位数字为 123 的第一个幂指数，将迭代器增加 196。
    因为任意两个首位数字为 123 的幂指数之差都大于或等于 196。
    增加 196 后得到 286。

    log_difference(286) = 0.09457875989861，大于上界。
    下一个幂指数是 379，需要增加 93 才能到达。
    此时迭代器变为 379，它是下一个首位数字为 123 的幂指数。

    再以 1060 为例。增加 196，得到 1256。
    log_difference(1256) = 0.09367455396034,
    该值大于上界，因此增加 93。此时迭代器为 1349。
    log_difference(1349) = 0.08946415071057，小于下界。
    下一个幂指数是 1545，需要增加 196 才能得到 1545。

    条件如下：

    1) 如果某个幂指数的 log_difference() 位于下界与上界之间，
    则增加 196。这意味着该幂指数对应的数以 123 开头。
    2) 如果某个幂指数的 log_difference() 大于或等于上界，则增加 93。
    3) 如果 log_difference() < lowerbound，则增加 196。

    上述逻辑的参考资料：
    https://math.stackexchange.com/questions/4093970/powers-of-2-starting-with-123-does-a-pattern-exist

    >>> solution(1000)
    284168

    >>> solution(56000)
    15924915

    >>> solution(678910)
    193060223

    """

    power_iterator = 90
    position = 0

    lower_limit = math.log(1.23, 10)
    upper_limit = math.log(1.24, 10)
    previous_power = 0

    while position < number:
        difference = log_difference(power_iterator)

        if difference >= upper_limit:
            power_iterator += 93

        elif difference < lower_limit:
            power_iterator += 196

        else:
            previous_power = power_iterator
            power_iterator += 196
            position += 1

    return previous_power


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print(f"{solution() = }")
