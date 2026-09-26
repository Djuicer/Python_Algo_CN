"""
插入排序（Insertion Sort）算法的纯 Python 实现

通过比较相邻元素对集合排序。
发现顺序不正确时，将当前元素向前移动，
直到顺序正确。然后直接返回该元素的
初始位置，继续向后比较。

运行 doctest 请使用以下命令：
python3 -m doctest -v insertion_sort.py

手动测试请运行：
python3 insertion_sort.py
"""

from collections.abc import MutableSequence
from typing import Any, Protocol, TypeVar


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=Comparable)


def insertion_sort[T: Comparable](collection: MutableSequence[T]) -> MutableSequence[T]:
    """插入排序算法的纯 Python 实现

    :param collection: 可变有序集合，其中包含类型可不同但
    可相互比较的元素
    :return: 按升序排列后的同一个集合

    复杂度分析：
        时间复杂度：
            - 最好情况：集合已有序时为 O(n)
            - 平均情况：O(n^2)
            - 最坏情况：集合逆序时为 O(n^2)

        空间复杂度：
            - O(1)，因为算法原地排序，
              仅使用常数大小的额外内存

    示例：
    >>> insertion_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> insertion_sort([]) == sorted([])
    True
    >>> insertion_sort([-2, -5, -45]) == sorted([-2, -5, -45])
    True
    >>> insertion_sort(['d', 'a', 'b', 'e', 'c']) == sorted(['d', 'a', 'b', 'e', 'c'])
    True
    >>> values = [4, 2, 7, 1]
    >>> result = insertion_sort(values)
    >>> result is values
    True
    >>> values
    [1, 2, 4, 7]
    >>> import random
    >>> collection = random.sample(range(-50, 50), 100)
    >>> insertion_sort(collection) == sorted(collection)
    True
    >>> import string
    >>> collection = random.choices(string.ascii_letters + string.digits, k=100)
    >>> insertion_sort(collection) == sorted(collection)
    True
    """

    for insert_index in range(1, len(collection)):
        insert_value = collection[insert_index]
        while insert_index > 0 and insert_value < collection[insert_index - 1]:
            collection[insert_index] = collection[insert_index - 1]
            insert_index -= 1
        collection[insert_index] = insert_value
    return collection


if __name__ == "__main__":
    from doctest import testmod

    testmod()

    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    print(f"{insertion_sort(unsorted) = }")
