"""
Project Euler Problem 27
https://projecteuler.net/problem=27

题目说明：

Euler 发现了一个非凡的二次公式：
n2 + n + 41
事实证明，当 n 连续取 0 到 39 时，该公式会产生 40 个素数。然而，当 n = 40 时，
402 + 40 + 41 = 40(40 + 1) + 41 可被 41 整除；当 n = 41 时，
412 + 41 + 41 显然也可被 41 整除。
后来发现了惊人的公式 n2 - 79n + 1601，当 n 连续取 0 到 79 时会产生 80 个素数。
系数 -79 和 1601 的乘积为 -126479。
考虑如下形式的二次式：
n² + an + b，其中 |a| &lt; 1000 且 |b| &lt; 1000
其中 |n| 表示 n 的模或绝对值，例如 |11| = 11 且 |-4| = 4。
求从 n = 0 开始连续取值时能产生最多素数的二次表达式中，系数 a 和 b 的乘积。
"""

import math


def is_prime(number: int) -> bool:
    """以 O(sqrt(n)) 的时间复杂度检查一个数是否为素数。
    如果一个数恰好有两个因数（1 和它本身），则它是素数。
    返回表示给定数字 num 是否为素数的布尔值。

    >>> is_prime(2)
    True
    >>> is_prime(3)
    True
    >>> is_prime(27)
    False
    >>> is_prime(2999)
    True
    >>> is_prime(0)
    False
    >>> is_prime(1)
    False
    >>> is_prime(-10)
    False
    """

    if 1 < number < 4:
        # 2 和 3 是质数
        return True
    elif number < 2 or number % 2 == 0 or number % 3 == 0:
        # 负数、0、1、所有偶数以及 3 的倍数都不是质数
        return False

    # 所有质数都形如 6k +/- 1
    for i in range(5, int(math.sqrt(number) + 1), 6):
        if number % i == 0 or number % (i + 2) == 0:
            return False
    return True


def solution(a_limit: int = 1000, b_limit: int = 1000) -> int:
    """
    >>> solution(1000, 1000)
    -59231
    >>> solution(200, 1000)
    -59231
    >>> solution(200, 200)
    -4925
    >>> solution(-1000, 1000)
    0
    >>> solution(-1000, -1000)
    0
    """
    longest = [0, 0, 0]  # length, a, b
    for a in range((a_limit * -1) + 1, a_limit):
        for b in range(2, b_limit):
            if is_prime(b):
                count = 0
                n = 0
                while is_prime((n**2) + (a * n) + b):
                    count += 1
                    n += 1
                if count > longest[0]:
                    longest = [count, a, b]
    ans = longest[1] * longest[2]
    return ans


if __name__ == "__main__":
    print(solution(1000, 1000))
