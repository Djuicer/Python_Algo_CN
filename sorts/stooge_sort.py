from typing import Protocol


class Comparable(Protocol):
    def __lt__(self, other: object, /) -> bool: ...


def stooge_sort[T: Comparable](arr: list[T]) -> list[T]:
    """
    示例：
    >>> stooge_sort([18.1, 0, -7.1, -1, 2, 2])
    [-7.1, -1, 0, 2, 2, 18.1]

    >>> stooge_sort([])
    []

    >>> stooge_sort(["c", "a", "b"])
    ['a', 'b', 'c']

    >>> stooge_sort([2.5, -1, 0.0])
    [-1, 0.0, 2.5]

    >>> stooge_sort([1, "a"])
    Traceback (most recent call last):
    ...
    TypeError: '<' not supported between instances of 'str' and 'int'
    """
    stooge(arr, 0, len(arr) - 1)
    return arr


def stooge[T: Comparable](arr: list[T], i: int, h: int) -> None:
    if i >= h:
        return

    # 如果首元素小于末元素，则交换两者
    if arr[h] < arr[i]:
        arr[i], arr[h] = arr[h], arr[i]

    # 数组中有超过 2 个元素时
    if h - i + 1 > 2:
        t = (int)((h - i + 1) / 3)

        # 递归排序前 2/3 的元素
        stooge(arr, i, (h - t))

        # 递归排序后 2/3 的元素
        stooge(arr, i + t, (h))

        # 递归排序前 2/3 的元素
        stooge(arr, i, (h - t))


if __name__ == "__main__":
    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    print(stooge_sort(unsorted))
