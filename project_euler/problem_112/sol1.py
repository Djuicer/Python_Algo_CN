"""
Problem 112: https://projecteuler.net/problem=112

从左到右观察，如果任一数字都不大于其左侧数字，则称为递增数；例如 134468。
类似地，如果任一数字都不大于其右侧数字，则称为递减数；例如 66420。
既非递增也非递减的正整数称为“弹跳数”，例如 155349。
显然，一百以下不存在弹跳数，但一千以下的数中略多于一半（525）是弹跳数。
事实上，弹跳数比例首次达到 50% 时的最小数是 538。令人惊讶的是，弹跳数越来越常见，
到 21780 时，弹跳数比例达到 90%。

找出弹跳数比例恰好为 99% 时的最小数。
"""


def check_bouncy(n: int) -> bool:
    """
    如果 number 是弹跳数则返回 True，否则返回 False。
    >>> check_bouncy(6789)
    False
    >>> check_bouncy(-12345)
    False
    >>> check_bouncy(0)
    False
    >>> check_bouncy(6.74)
    Traceback (most recent call last):
        ...
    ValueError: check_bouncy() accepts only integer arguments
    >>> check_bouncy(132475)
    True
    >>> check_bouncy(34)
    False
    >>> check_bouncy(341)
    True
    >>> check_bouncy(47)
    False
    >>> check_bouncy(-12.54)
    Traceback (most recent call last):
        ...
    ValueError: check_bouncy() accepts only integer arguments
    >>> check_bouncy(-6548)
    True
    """
    if not isinstance(n, int):
        raise ValueError("check_bouncy() accepts only integer arguments")
    str_n = str(n)
    sorted_str_n = "".join(sorted(str_n))
    return str_n not in {sorted_str_n, sorted_str_n[::-1]}


def solution(percent: float = 99) -> int:
    """
    返回弹跳数比例恰好为 'percent' 时的最小数。
    >>> solution(50)
    538
    >>> solution(90)
    21780
    >>> solution(80)
    4770
    >>> solution(105)
    Traceback (most recent call last):
        ...
    ValueError: solution() only accepts values from 0 to 100
    >>> solution(100.011)
    Traceback (most recent call last):
        ...
    ValueError: solution() only accepts values from 0 to 100
    """
    if not 0 < percent < 100:
        raise ValueError("solution() only accepts values from 0 to 100")
    bouncy_num = 0
    num = 1

    while True:
        if check_bouncy(num):
            bouncy_num += 1
        if (bouncy_num / num) * 100 >= percent:
            return num
        num += 1


if __name__ == "__main__":
    from doctest import testmod

    testmod()
    print(f"{solution(99)}")
