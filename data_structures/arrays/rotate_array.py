def rotate_array(arr: list[int], steps: int) -> list[int]:
    """
    旋转一个 列表 到 右 通过 步骤 位置。

    参数：
    arr (列表[int]): 该列表 的 整数 到 旋转。
    步骤 (int): 数 的 位置 到 旋转. 可以 为 负 用于 左 旋转。

    返回值：
    列表[int]: Rotated 列表。

    示例：
    >>> rotate_array([1, 2, 3, 4, 5], 2)
    [4, 5, 1, 2, 3]
    >>> rotate_array([1, 2, 3, 4, 5], -2)
    [3, 4, 5, 1, 2]
    >>> rotate_array([1, 2, 3, 4, 5], 7)
    [4, 5, 1, 2, 3]
    >>> rotate_array([], 3)
    []
    """

    n = len(arr)
    if n == 0:
        return arr

    steps = steps % n

    if steps < 0:
        steps += n

    def reverse(start: int, end: int) -> None:
        """
        Reverses portion 的列表 原地 从 索引 开始 到 末尾。

        参数：
        开始 (int): 起始 索引 的 portion 到 反转。
        末尾 (int): Ending 索引 的 portion 到 反转。

        返回值：
        None

        示例：
        >>> example = [1, 2, 3, 4, 5]
        >>> def reverse_test(arr, start, end):
        ...     while start < end:
        ...         arr[start], arr[end] = arr[end], arr[start]
        ...         start += 1
        ...         end -= 1
        >>> reverse_test(example, 0, 2)
        >>> example
        [3, 2, 1, 4, 5]
        >>> reverse_test(example, 2, 4)
        >>> example
        [3, 2, 5, 4, 1]
        """

        while start < end:
            arr[start], arr[end] = arr[end], arr[start]
            start += 1
            end -= 1

    reverse(0, n - 1)
    reverse(0, steps - 1)
    reverse(steps, n - 1)

    return arr


if __name__ == "__main__":
    examples = [
        ([1, 2, 3, 4, 5], 2),
        ([1, 2, 3, 4, 5], -2),
        ([1, 2, 3, 4, 5], 7),
        ([], 3),
    ]

    for arr, steps in examples:
        rotated = rotate_array(arr.copy(), steps)
        print(f"Rotate {arr} by {steps}: {rotated}")
