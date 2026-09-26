def get_1s_count(number: int) -> int:
    """
    使用 Brian Kernighan 方法统计 32 位整数中置位比特的数量。
    参考资料：https://graphics.stanford.edu/~seander/bithacks.html#CountBitsSetKernighan
    >>> get_1s_count(25)
    3
    >>> get_1s_count(37)
    3
    >>> get_1s_count(21)
    3
    >>> get_1s_count(58)
    4
    >>> get_1s_count(0)
    0
    >>> get_1s_count(256)
    1
    >>> get_1s_count(-1)
    Traceback (most recent call last):
        ...
    ValueError: Input must be a non-negative integer
    >>> get_1s_count(0.8)
    Traceback (most recent call last):
        ...
    ValueError: Input must be a non-negative integer
    >>> get_1s_count("25")
    Traceback (most recent call last):
        ...
    ValueError: Input must be a non-negative integer
    """
    if not isinstance(number, int) or number < 0:
        raise ValueError("Input must be a non-negative integer")

    count = 0
    while number:
        # 此方法直接到达下一个置位比特（下一个 1），而不是遍历每一位并检查 1，
        # 因此循环不会运行 32 次，而只会运行与 `1` 的数量相同的次数。
        number &= number - 1
        count += 1
    return count


if __name__ == "__main__":
    import doctest

    doctest.testmod()
