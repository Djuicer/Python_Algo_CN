from typing import Any, Protocol, TypeVar


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=Comparable)


def bubble_sort_iterative[T: Comparable](collection: list[T]) -> list[T]:
    """冒泡排序（Bubble Sort）算法的纯 Python 实现（迭代版本）。

    冒泡排序反复遍历集合，
    比较每对相邻元素，并在顺序
    不正确时交换。每一轮完整遍历
    都会将未排序部分中最大的元素“冒泡”到
    集合末尾的正确位置，直到某一轮
    没有发生交换，此时集合已排序。

    时间复杂度：最好情况为 O(n)（已有序，通过
    提前退出实现），平均和最坏情况为 O(n^2)。
    辅助空间复杂度：O(1)（原地排序）。

    :param collection: 可变有序集合，其中包含类型可不同但
    可相互比较的元素
    :return: 按升序排列后的同一个集合

    示例：
    >>> bubble_sort_iterative([0, 5, 2, 3, 2])
    [0, 2, 2, 3, 5]
    >>> bubble_sort_iterative([])
    []
    >>> bubble_sort_iterative([-2, -45, -5])
    [-45, -5, -2]
    >>> bubble_sort_iterative([-23, 0, 6, -4, 34])
    [-23, -4, 0, 6, 34]
    >>> bubble_sort_iterative([1, 2, 3, 4])
    [1, 2, 3, 4]
    >>> bubble_sort_iterative([3, 3, 3, 3])
    [3, 3, 3, 3]
    >>> bubble_sort_iterative([56])
    [56]
    >>> bubble_sort_iterative([0, 5, 2, 3, 2]) == sorted([0, 5, 2, 3, 2])
    True
    >>> bubble_sort_iterative([]) == sorted([])
    True
    >>> bubble_sort_iterative([-2, -45, -5]) == sorted([-2, -45, -5])
    True
    >>> bubble_sort_iterative([-23, 0, 6, -4, 34]) == sorted([-23, 0, 6, -4, 34])
    True
    >>> bubble_sort_iterative(['d', 'a', 'b', 'e']) == sorted(['d', 'a', 'b', 'e'])
    True
    >>> bubble_sort_iterative(['z', 'a', 'y', 'b', 'x', 'c'])
    ['a', 'b', 'c', 'x', 'y', 'z']
    >>> bubble_sort_iterative([1.1, 3.3, 5.5, 7.7, 2.2, 4.4, 6.6])
    [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7]
    >>> bubble_sort_iterative([1, 3.3, 5, 7.7, 2, 4.4, 6])
    [1, 2, 3.3, 4.4, 5, 6, 7.7]
    >>> import random
    >>> collection_arg = random.sample(range(-50, 50), 100)
    >>> bubble_sort_iterative(collection_arg) == sorted(collection_arg)
    True
    >>> import string
    >>> collection_arg = random.choices(string.ascii_letters + string.digits, k=100)
    >>> bubble_sort_iterative(collection_arg) == sorted(collection_arg)
    True
    >>> bubble_sort_iterative([1, "a"])  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: '<' not supported between instances of 'str' and 'int'
    """
    length = len(collection)
    for i in reversed(range(length)):
        swapped = False
        for j in range(i):
            if collection[j] > collection[j + 1]:
                swapped = True
                collection[j], collection[j + 1] = collection[j + 1], collection[j]
        if not swapped:
            break  # 集合已有序时停止迭代。
    return collection


def bubble_sort_recursive[T: Comparable](collection: list[T]) -> list[T]:
    """冒泡排序算法的纯 Python 实现（递归版本）。

    功能与迭代版本相同：每次调用完整遍历
    集合一次，比较相邻元素，
    交换顺序不正确的元素对。若本轮发生交换，
    则对部分排序后的集合再次递归调用；
    某一轮没有交换时，集合已排序，
    递归停止。

    时间复杂度：最好情况为 O(n)（已有序），平均和
    最坏情况为 O(n^2)。
    排序本身的辅助空间复杂度为 O(1)（原地排序），
    但递归在最坏情况下会增加 O(n) 个调用栈帧。

    :param collection: 可变有序元素序列
    :return: 按升序排列后的同一个列表

    示例：
    >>> bubble_sort_recursive([0, 5, 2, 3, 2])
    [0, 2, 2, 3, 5]
    >>> bubble_sort_recursive([])
    []
    >>> bubble_sort_recursive([-2, -45, -5])
    [-45, -5, -2]
    >>> bubble_sort_recursive([-23, 0, 6, -4, 34])
    [-23, -4, 0, 6, 34]
    >>> bubble_sort_recursive([0, 5, 2, 3, 2]) == sorted([0, 5, 2, 3, 2])
    True
    >>> bubble_sort_recursive([]) == sorted([])
    True
    >>> bubble_sort_recursive([-2, -45, -5]) == sorted([-2, -45, -5])
    True
    >>> bubble_sort_recursive([-23, 0, 6, -4, 34]) == sorted([-23, 0, 6, -4, 34])
    True
    >>> bubble_sort_recursive(['d', 'a', 'b', 'e']) == sorted(['d', 'a', 'b', 'e'])
    True
    >>> bubble_sort_recursive(['z', 'a', 'y', 'b', 'x', 'c'])
    ['a', 'b', 'c', 'x', 'y', 'z']
    >>> bubble_sort_recursive([1.1, 3.3, 5.5, 7.7, 2.2, 4.4, 6.6])
    [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7]
    >>> bubble_sort_recursive([1, 3.3, 5, 7.7, 2, 4.4, 6])
    [1, 2, 3.3, 4.4, 5, 6, 7.7]
    >>> bubble_sort_recursive(['a', 'Z', 'B', 'C', 'A', 'c'])
    ['A', 'B', 'C', 'Z', 'a', 'c']
    >>> import random
    >>> collection_arg = random.sample(range(-50, 50), 100)
    >>> bubble_sort_recursive(collection_arg) == sorted(collection_arg)
    True
    >>> import string
    >>> collection_arg = random.choices(string.ascii_letters + string.digits, k=100)
    >>> bubble_sort_recursive(collection_arg) == sorted(collection_arg)
    True
    >>> bubble_sort_recursive([1, "a"])  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: '<' not supported between instances of 'str' and 'int'
    """
    length = len(collection)
    swapped = False
    for i in range(length - 1):
        if collection[i] > collection[i + 1]:
            collection[i], collection[i + 1] = collection[i + 1], collection[i]
            swapped = True

    return collection if not swapped else bubble_sort_recursive(collection)


if __name__ == "__main__":
    import doctest
    from random import sample
    from timeit import timeit

    doctest.testmod()

    # 基准测试：迭代版本似乎略快于递归版本。
    num_runs = 10_000
    unsorted = sample(range(-50, 50), 100)
    timer_iterative = timeit(
        "bubble_sort_iterative(unsorted[:])", globals=globals(), number=num_runs
    )
    print("\nIterative bubble sort:")
    print(*bubble_sort_iterative(unsorted), sep=",")
    print(f"Processing time (iterative): {timer_iterative:.5f}s for {num_runs:,} runs")

    unsorted = sample(range(-50, 50), 100)
    timer_recursive = timeit(
        "bubble_sort_recursive(unsorted[:])", globals=globals(), number=num_runs
    )
    print("\nRecursive bubble sort:")
    print(*bubble_sort_recursive(unsorted), sep=",")
    print(f"Processing time (recursive): {timer_recursive:.5f}s for {num_runs:,} runs")
