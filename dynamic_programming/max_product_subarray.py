def max_product_subarray(numbers: list[int]) -> int:
    """
    返回给定整数列表 `numbers` 的连续子数组所能得到的最大乘积。

    示例：

    >>> max_product_subarray([2, 3, -2, 4])
    6
    >>> max_product_subarray((-2, 0, -1))
    0
    >>> max_product_subarray([2, 3, -2, 4, -1])
    48
    >>> max_product_subarray([-1])
    -1
    >>> max_product_subarray([0])
    0
    >>> max_product_subarray([])
    0
    >>> max_product_subarray("")
    0
    >>> max_product_subarray(None)
    0
    >>> max_product_subarray([2, 3, -2, 4.5, -1])
    Traceback (most recent call last):
        ...
    ValueError: numbers must be an iterable of integers
    >>> max_product_subarray("ABC")
    Traceback (most recent call last):
        ...
    ValueError: numbers must be an iterable of integers
    """
    if not numbers:
        return 0

    if not isinstance(numbers, (list, tuple)) or not all(
        isinstance(number, int) for number in numbers
    ):
        raise ValueError("numbers must be an iterable of integers")

    max_till_now = min_till_now = max_prod = numbers[0]

    for i in range(1, len(numbers)):
        # 更新子数组乘积的最大值和最小值
        number = numbers[i]
        if number < 0:
            max_till_now, min_till_now = min_till_now, max_till_now
        max_till_now = max(number, max_till_now * number)
        min_till_now = min(number, min_till_now * number)

        # 更新目前找到的最大乘积
        max_prod = max(max_prod, max_till_now)

    return max_prod
