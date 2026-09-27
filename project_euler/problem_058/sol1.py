"""
Project Euler Problem 58:https://projecteuler.net/problem=58


从 1 开始，按如下方式逆时针旋转，可形成边长为 7 的方形螺旋。

37 36 35 34 33 32 31
38 17 16 15 14 13 30
39 18  5  4  3 12 29
40 19  6  1  2 11 28
41 20  7  8  9 10 27
42 21 22 23 24 25 26
43 44 45 46 47 48 49

值得注意的是，奇数的平方位于右下对角线上；更有趣的是，两条对角线上的 13 个数中
有 8 个是素数，即比例为 8/13 ≈ 62%。

如果在上述螺旋外围完整包上一层，将形成边长为 9 的方形螺旋。
若继续此过程，两条对角线上的素数比例首次低于 10% 时，方形螺旋的边长是多少？

解法：需要找到使比例低于 10% 的奇数边长。每增加一层，对角线上就增加 4 个元素。
设已有边长为奇数 j 的方形螺旋，从 j 增加到 j+2 时，新增
j*j+j+1,j*j+2*(j+1),j*j+3*(j+1),j*j+4*(j+1)。
这 4 个数中只有前三个可能成为素数，因为最后一个可化为 (j+2)*(j+2)。
因此，在增加当前素数计数前，逐一检查前三个数。

"""

import math


def is_prime(number: int) -> bool:
    """以 O(sqrt(n)) 的时间复杂度检查一个数是否为素数。

    如果一个数恰好有两个因数（1 和它本身），则它是素数。

    >>> is_prime(0)
    False
    >>> is_prime(1)
    False
    >>> is_prime(2)
    True
    >>> is_prime(3)
    True
    >>> is_prime(27)
    False
    >>> is_prime(87)
    False
    >>> is_prime(563)
    True
    >>> is_prime(2999)
    True
    >>> is_prime(67483)
    False
    """

    if 1 < number < 4:
        # 2 and 3 are primes
        return True
    elif number < 2 or number % 2 == 0 or number % 3 == 0:
        # Negatives, 0, 1, all even numbers, all multiples of 3 are not primes
        return False

    # All primes number are in format of 6k +/- 1
    for i in range(5, int(math.sqrt(number) + 1), 6):
        if number % i == 0 or number % (i + 2) == 0:
            return False
    return True


def solution(ratio: float = 0.1) -> int:
    """
    返回大于 1 的奇数边长方形螺旋中，两条对角线上的素数比例首次低于给定比例时的边长。
    >>> solution(.5)
    11
    >>> solution(.2)
    309
    >>> solution(.111)
    11317
    """

    j = 3
    primes = 3

    while primes / (2 * j - 1) >= ratio:
        for i in range(j * j + j + 1, (j + 2) * (j + 2), j + 1):
            primes += is_prime(i)
        j += 2
    return j


if __name__ == "__main__":
    import doctest

    doctest.testmod()
