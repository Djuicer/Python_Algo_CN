def actual_power(a: int, b: int) -> int:
    """
    使用分治法计算 a^b。
    仅适用于整数 a、b。

    :param a: 幂运算的底数，为整数。
    :param b: 幂运算的指数，为非负整数。
    :return: a^b 的结果。

    示例：
    >>> actual_power(3, 2)
    9
    >>> actual_power(5, 3)
    125
    >>> actual_power(2, 5)
    32
    >>> actual_power(7, 0)
    1
    """
    if b == 0:
        return 1
    half = actual_power(a, b // 2)

    if (b % 2) == 0:
        return half * half
    else:
        return a * half * half


def power(a: int, b: int) -> float:
    """
    :param a: 底数（整数）。
    :param b: 指数（整数）。
    :return: a^b 的结果；指数为负时返回浮点数。

    >>> power(4,6)
    4096
    >>> power(2,3)
    8
    >>> power(-2,3)
    -8
    >>> power(2,-3)
    0.125
    >>> power(-2,-3)
    -0.125
    """
    if b < 0:
        return 1 / actual_power(a, -b)
    return actual_power(a, b)


if __name__ == "__main__":
    print(power(-2, -3))  # output -0.125
