from __future__ import annotations

arr = [-10, -5, 0, 5, 5.1, 11, 13, 21, 3, 4, -21, -10, -5, -1, 0]
expect = [-5, 0, 5, 5.1, 11, 13, 21, -1, 4, -1, -10, -5, -1, 0, -1]


def next_greatest_element_slow(arr: list[float]) -> list[float]:
    """
    获取 下一个 Greatest 元素 (NGE) 用于 每个元素 在 该数组
    通过 checking 所有 subsequent 元素 到 查找 下一个 更大 一个。

    此 是 brute-force 实现，并且 它 具有 时间复杂度
    的 O(n^2)，其中 n 是 大小 的 该数组。

    参数：
        arr: 列表 的 数 用于 其 NGE 是 计算得出。

    返回值：
        列表 包含 下一个 greatest 元素. 如果 没有
        更大 元素 是 找到，-1 是 placed 在 结果。

    示例：
    >>> next_greatest_element_slow(arr) == expect
    True
    """

    result = []
    arr_size = len(arr)

    for i in range(arr_size):
        next_element: float = -1
        for j in range(i + 1, arr_size):
            if arr[i] < arr[j]:
                next_element = arr[j]
                break
        result.append(next_element)
    return result


def next_greatest_element_fast(arr: list[float]) -> list[float]:
    """
    查找 下一个 Greatest 元素 (NGE) 用于 每个元素 在 该数组
    使用 更多 readable 方法. 此 实现 utilizes
    enumerate() 用于 outer 循环 并且 slicing 用于 inner 循环。

    当 此 improves readability 超过 next_greatest_element_slow(),
    它 仍然 具有 时间复杂度 的 O(n^2)。

    参数：
        arr: 列表 的 数 用于 其 NGE 是 计算得出。

    返回值：
        列表 包含 下一个 greatest 元素. 如果 没有
        更大 元素 是 找到，-1 是 placed 在 结果。

    示例：
    >>> next_greatest_element_fast(arr) == expect
    True
    """
    result = []
    for i, outer in enumerate(arr):
        next_item: float = -1
        for inner in arr[i + 1 :]:
            if outer < inner:
                next_item = inner
                break
        result.append(next_item)
    return result


def next_greatest_element(arr: list[float]) -> list[float]:
    """
    Efficient 解 到 查找 下一个 Greatest 元素 (NGE) 用于 所有元素
    使用 栈. 时间复杂度 是 reduced 到 O(n)，making 它 suitable
    用于 larger 数组。

    该栈 保持 track 的 元素 用于 其 下一个 更大 元素 hasn't
    been 找到 yet. 通过 iterating 通过 该数组 在 反转 (从 最后一个
    元素 到 第一个)，该栈 是 使用 到 efficiently determine 下一个
    greatest 元素 用于 每个元素。

    参数：
        arr: 列表 的 数 用于 其 NGE 是 计算得出。

    返回值：
        列表 包含 下一个 greatest 元素. 如果 没有
        更大 元素 是 找到，-1 是 placed 在 结果。

    示例：
    >>> next_greatest_element(arr) == expect
    True
    """
    arr_size = len(arr)
    stack: list[float] = []
    result: list[float] = [-1] * arr_size

    for index in reversed(range(arr_size)):
        if stack:
            while stack[-1] <= arr[index]:
                stack.pop()
                if not stack:
                    break
        if stack:
            result[index] = stack[-1]
        stack.append(arr[index])
    return result


if __name__ == "__main__":
    from doctest import testmod
    from timeit import timeit

    testmod()
    print(next_greatest_element_slow(arr))
    print(next_greatest_element_fast(arr))
    print(next_greatest_element(arr))

    setup = (
        "from __main__ import arr, next_greatest_element_slow, "
        "next_greatest_element_fast, next_greatest_element"
    )
    print(
        "next_greatest_element_slow():",
        timeit("next_greatest_element_slow(arr)", setup=setup),
    )
    print(
        "next_greatest_element_fast():",
        timeit("next_greatest_element_fast(arr)", setup=setup),
    )
    print(
        "     next_greatest_element():",
        timeit("next_greatest_element(arr)", setup=setup),
    )
