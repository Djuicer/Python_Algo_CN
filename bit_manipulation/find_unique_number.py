def find_unique_number(arr: list[int]) -> int:
    """
    给定一个整数列表，其中除一个元素外，其余元素均出现两次；
    此函数使用按位异或返回仅出现一次的元素。

    >>> find_unique_number([1, 1, 2, 2, 3])
    3
    >>> find_unique_number([4, 5, 4, 6, 6])
    5
    >>> find_unique_number([7])
    7
    >>> find_unique_number([10, 20, 10])
    20
    >>> find_unique_number([])
    Traceback (most recent call last):
        ...
    ValueError: input list must not be empty
    >>> find_unique_number([1, 'a', 1])
    Traceback (most recent call last):
        ...
    TypeError: all elements must be integers
    """
    if not arr:
        raise ValueError("input list must not be empty")
    if not all(isinstance(x, int) for x in arr):
        raise TypeError("all elements must be integers")

    result = 0
    for num in arr:
        result ^= num
    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
