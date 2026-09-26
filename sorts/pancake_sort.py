"""煎饼排序（Pancake Sort）算法实现。

煎饼排序算法的纯 Python 实现。
煎饼排序通过反复翻转数组片段对数组排序，
类似于在一叠煎饼中插入铲子，
翻转上面的一部分来调整顺序。

算法先找到最大元素，将其翻到顶端，
再翻到正确位置。对剩余未排序部分
重复该过程。

时间复杂度：O(n^2)，执行 n 轮，每轮最多翻转 2 次
空间复杂度：O(1)，原地排序，仅使用常数大小的额外空间

运行 doctest 请使用以下命令：
    python3 -m doctest -v pancake_sort.py
或
    python -m doctest -v pancake_sort.py
手动测试请运行：
    python pancake_sort.py
"""

from collections.abc import Sequence
from typing import Any, Protocol, TypeVar


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=Comparable)


def pancake_sort[T: Comparable](arr: Sequence[T]) -> list[T]:
    """使用煎饼排序对数组排序。

    :param arr: 有序集合，其中包含类型可不同但可相互比较的
    元素
    :return: 按升序排列后的同一个集合

    时间复杂度：(O(n^2))
    空间复杂度：(O(n))

    示例：
    >>> pancake_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> pancake_sort([])
    []
    >>> pancake_sort([-2, -5, -45])
    [-45, -5, -2]
    >>> pancake_sort(['d', 'a', 'b', 'e', 'c']) == sorted(['d', 'a', 'b', 'e', 'c'])
    True
    >>> import random
    >>> collection = random.sample(range(-50, 50), 100)
    >>> pancake_sort(collection) == sorted(collection)
    True
    >>> import string
    >>> collection = random.choices(string.ascii_letters + string.digits, k=100)
    >>> pancake_sort(collection) == sorted(collection)
    True
    """
    arr = list(arr)
    cur = len(arr)
    while cur > 1:
        # 查找 arr[0:cur] 中最大元素的索引
        max_index = arr.index(max(arr[:cur]))
        # 将最大元素移到当前未排序部分的末尾：
        # 1. 翻转，将最大元素移到开头
        arr[: max_index + 1] = reversed(arr[: max_index + 1])
        # 2. 再次翻转，将最大元素移到 cur-1
        arr[:cur] = reversed(arr[:cur])
        cur -= 1
    return arr


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    print(f"{unsorted = }, {pancake_sort(unsorted) = }")
