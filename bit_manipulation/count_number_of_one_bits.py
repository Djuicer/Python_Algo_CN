from timeit import timeit


def get_set_bits_count_using_brian_kernighans_algorithm(number: int) -> int:
    """
    统计 32 位整数中置位比特的数量。
    >>> get_set_bits_count_using_brian_kernighans_algorithm(25)
    3
    >>> get_set_bits_count_using_brian_kernighans_algorithm(37)
    3
    >>> get_set_bits_count_using_brian_kernighans_algorithm(21)
    3
    >>> get_set_bits_count_using_brian_kernighans_algorithm(58)
    4
    >>> get_set_bits_count_using_brian_kernighans_algorithm(0)
    0
    >>> get_set_bits_count_using_brian_kernighans_algorithm(256)
    1
    >>> get_set_bits_count_using_brian_kernighans_algorithm(-1)
    Traceback (most recent call last):
        ...
    ValueError: the value of input must not be negative
    >>> get_set_bits_count_using_brian_kernighans_algorithm(1023)
    10
    """
    if number < 0:
        raise ValueError("the value of input must not be negative")
    result = 0
    while number:
        number &= number - 1
        result += 1
    return result


def get_set_bits_count_using_modulo_operator(number: int) -> int:
    """
    统计 32 位整数中置位比特的数量。
    >>> get_set_bits_count_using_modulo_operator(25)
    3
    >>> get_set_bits_count_using_modulo_operator(37)
    3
    >>> get_set_bits_count_using_modulo_operator(21)
    3
    >>> get_set_bits_count_using_modulo_operator(58)
    4
    >>> get_set_bits_count_using_modulo_operator(0)
    0
    >>> get_set_bits_count_using_modulo_operator(256)
    1
    >>> get_set_bits_count_using_modulo_operator(-1)
    Traceback (most recent call last):
        ...
    ValueError: the value of input must not be negative
    >>> get_set_bits_count_using_modulo_operator(1024)
    1
    """
    if number < 0:
        raise ValueError("the value of input must not be negative")
    result = 0
    while number:
        if number % 2 == 1:
            result += 1
        number >>= 1
    return result


def get_set_bits_count_using_lookup_table(number: int) -> int:
    """
    使用预先计算的查找表统计 32 位整数中置位比特的数量。

    GeeksforGeeks 中有类似方法，但实现不同。
    代码链接：
    https://www.geeksforgeeks.org/dsa/count-set-bits-integer-using-lookup-table/

    >>> get_set_bits_count_using_lookup_table(25)
    3
    >>> get_set_bits_count_using_lookup_table(37)
    3
    >>> get_set_bits_count_using_lookup_table(21)
    3
    >>> get_set_bits_count_using_lookup_table(58)
    4
    >>> get_set_bits_count_using_lookup_table(0)
    0
    >>> get_set_bits_count_using_lookup_table(256)
    1
    >>> get_set_bits_count_using_lookup_table(-1)
    Traceback (most recent call last):
        ...
    ValueError: the value of input must not be negative
    """
    _lookup_table = [bin(i).count("1") for i in range(256)]

    if number < 0:
        raise ValueError("the value of input must not be negative")

    # 将 32 位数拆分为四个 8 位块，并使用查找表
    return (
        _lookup_table[number & 0xFF]
        + _lookup_table[(number >> 8) & 0xFF]
        + _lookup_table[(number >> 16) & 0xFF]
        + _lookup_table[(number >> 24) & 0xFF]
    )


def benchmark() -> None:
    """
    使用不同位数的整数比较三个函数的基准测试代码。
    Brian Kernighan 算法始终比 modulo_operator 更快，
    对于重复调用，查找表法通常最快。
    """

    def do_benchmark(number: int) -> None:
        setup = "import __main__ as z"
        print(f"Benchmark when {number = }:")

        print(f"{get_set_bits_count_using_modulo_operator(number) = }")
        timing = timeit(
            f"z.get_set_bits_count_using_modulo_operator({number})", setup=setup
        )
        print(f"timeit() runs in {timing} seconds")

        print(f"{get_set_bits_count_using_brian_kernighans_algorithm(number) = }")
        timing = timeit(
            f"z.get_set_bits_count_using_brian_kernighans_algorithm({number})",
            setup=setup,
        )
        print(f"timeit() runs in {timing} seconds")

        print(f"{get_set_bits_count_using_lookup_table(number) = }")
        timing = timeit(
            f"z.get_set_bits_count_using_lookup_table({number})",
            setup=setup,
        )
        print(f"timeit() runs in {timing} seconds")

    for number in (25, 37, 58, 0):
        do_benchmark(number)
        print()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
