from typing import Protocol


class Comparable(Protocol):
    def __lt__(self, other: object, /) -> bool: ...


def double_sort[T: Comparable](collection: list[T]) -> list[T]:
    """此算法使用冒泡排序的原理对数组排序，
    但同时进行从左到右和从右到左的遍历。
    因此称为“双向排序”（Double Sort）
    :param collection: 元素可比较的可变有序序列
    :return: 按升序排列后的同一个集合
    示例：
    >>> double_sort([-1 ,-2 ,-3 ,-4 ,-5 ,-6 ,-7])
    [-7, -6, -5, -4, -3, -2, -1]
    >>> double_sort([])
    []
    >>> double_sort([-1 ,-2 ,-3 ,-4 ,-5 ,-6])
    [-6, -5, -4, -3, -2, -1]
    >>> double_sort([-3, 10, 16, -42, 29]) == sorted([-3, 10, 16, -42, 29])
    True
    >>> double_sort(["c", "a", "b"])
    ['a', 'b', 'c']
    >>> double_sort([2.5, -1, 0.0])
    [-1, 0.0, 2.5]
    >>> double_sort([1, "a"])
    Traceback (most recent call last):
    ...
    TypeError: '<' not supported between instances of 'str' and 'int'
    """
    no_of_elements = len(collection)
    for _ in range(
        int(((no_of_elements - 1) / 2) + 1)
    ):  # 无需遍历到列表末尾，因为
        for j in range(no_of_elements - 1):
            # 从左到右（正向）执行冒泡排序
            if collection[j + 1] < collection[j]:
                collection[j], collection[j + 1] = collection[j + 1], collection[j]
            # 从右到左（反向）执行冒泡排序
            if collection[no_of_elements - 1 - j] < collection[no_of_elements - 2 - j]:
                (
                    collection[no_of_elements - 1 - j],
                    collection[no_of_elements - 2 - j],
                ) = (
                    collection[no_of_elements - 2 - j],
                    collection[no_of_elements - 1 - j],
                )
    return collection


if __name__ == "__main__":
    # 允许用户在一行中输入列表元素
    unsorted = [int(x) for x in input("Enter the list to be sorted: ").split() if x]
    print("the sorted list is")
    print(f"{double_sort(unsorted) = }")
