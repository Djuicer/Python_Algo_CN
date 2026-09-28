"""
在-位置 数组 reversal 该 也 返回值 reversed 列表 到 caller。
此 算法 反转 元素 的 一个列表 不使用 使用 extra 空间。
"""

from typing import Any


def reverse_array(arr: list[Any]) -> list[Any]:
    """
    Reverses 一个列表 在-位置。

    此函数 takes 一个列表 并且 reverses 其 元素 使用 两个-指针
    方法. 左 指针 starts 在 列表开头，并且
    右 指针 starts 在 末尾. 元素 在 这些 两个 指针 是
    swapped，并且 指针 移动 towards center until they meet 或 cross。

    参数：
        arr: 该列表 到 为 reversed。

    返回值：
        相同 列表，现在 reversed. 此 允许 用于 方法 chaining。

    Doctests:
    >>> reverse_array([1, 2, 3, 4, 5])
    [5, 4, 3, 2, 1]
    >>> reverse_array(['a', 'b', 'c', 'd'])
    ['d', 'c', 'b', 'a']
    >>> reverse_array([10.5, 20.2, 30.8])
    [30.8, 20.2, 10.5]
    >>> reverse_array(["apple", "banana", "cherry"])
    ['cherry', 'banana', 'apple']
    >>> reverse_array([1])
    [1]
    >>> reverse_array([])
    []
    >>> reverse_array(list(range(5)))
    [4, 3, 2, 1, 0]
    >>> reverse_array(tuple(range(5)))
    Traceback (most recent call last):
        ...
    TypeError: 'tuple' object does not support item assignment
    >>> reverse_array(range(5))
    Traceback (most recent call last):
        ...
    TypeError: 'range' object does not support item assignment
    """
    left = 0
    right = len(arr) - 1

    while left < right:
        # 交换 元素 在 左 并且 右 指针
        arr[left], arr[right] = arr[right], arr[left]
        # 移动 指针 towards center
        left += 1
        right -= 1
    return arr


if __name__ == "__main__":
    # doctest module runs 测试 embedded 在 函数's docstring。
    # 到 运行 测试，execute 此 script 从 命令 line：
    # python -m doctest -v reverse_array.py
    import doctest

    doctest.testmod()

    # 示例 usage：
    print("\n--- Example Usage ---")
    sample_array = [10, 20, 30, 40, 50, 60]
    print(f"{sample_array = }")
    print(f"{reverse_array(sample_array) = }")
