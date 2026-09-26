"""
跳跃查找（Jump Search）算法的纯 Python 实现。
该算法以 n^(1/2) 为步长遍历有序集合，
直到当前比较的元素大于目标元素。
然后执行线性查找，直到找到目标值。
未找到则返回 -1。

https://en.wikipedia.org/wiki/Jump_search
"""

import math
from collections.abc import Sequence
from typing import Any, Protocol


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


def jump_search[T: Comparable](arr: Sequence[T], item: T) -> int:
    """
    跳跃查找算法的 Python 实现。
    找到 `item` 则返回其索引，否则返回 -1。

    示例：
    >>> jump_search([0, 1, 2, 3, 4, 5], 3)
    3
    >>> jump_search([-5, -2, -1], -1)
    2
    >>> jump_search([0, 5, 10, 20], 8)
    -1
    >>> jump_search([0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610], 55)
    10
    >>> jump_search(["aa", "bb", "cc", "dd", "ee", "ff"], "ee")
    4
    >>> jump_search([], 1)
    -1
    """
    if not arr:
        return -1
    arr_size = len(arr)
    block_size = int(math.sqrt(arr_size))

    prev = 0
    step = block_size
    while arr[min(step, arr_size) - 1] < item:
        prev = step
        step += block_size
        if prev >= arr_size:
            return -1

    while arr[prev] < item:
        prev += 1
        if prev == min(step, arr_size):
            return -1
    if arr[prev] == item:
        return prev
    return -1


if __name__ == "__main__":
    user_input = input("Enter numbers separated by a comma:\n").strip()
    array = [int(item) for item in user_input.split(",")]
    x = int(input("Enter the number to be searched:\n"))

    res = jump_search(array, x)
    if res == -1:
        print("Number not found!")
    else:
        print(f"Number {x} is at index {res}")
