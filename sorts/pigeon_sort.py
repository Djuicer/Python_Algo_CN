"""
鸽巢排序（Pigeonhole Sort）的实现。
运行 doctest 请使用以下命令：

python3 -m doctest -v pigeon_sort.py
或
python -m doctest -v pigeon_sort.py

手动测试请运行：
python pigeon_sort.py
"""

from __future__ import annotations


def pigeon_sort(array: list[int]) -> list[int]:
    """
    鸽巢排序算法的实现
    :param array: 元素可比较的集合
    :return: 按升序排列的集合
    >>> pigeon_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> pigeon_sort([])
    []
    >>> pigeon_sort([-2, -5, -45])
    [-45, -5, -2]
    """
    if len(array) == 0:
        return array

    _min, _max = min(array), max(array)

    # 计算所需变量
    holes_range = _max - _min + 1
    holes, holes_repeat = [0] * holes_range, [0] * holes_range

    # 执行排序。
    for i in array:
        index = i - _min
        holes[index] = i
        holes_repeat[index] += 1

    # 通过替换数值重建数组。
    index = 0
    for i in range(holes_range):
        while holes_repeat[i] > 0:
            array[index] = holes[i]
            index += 1
            holes_repeat[i] -= 1

    # 返回排序后的数组。
    return array


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    user_input = input("Enter numbers separated by comma:\n")
    unsorted = [int(x) for x in user_input.split(",")]
    print(pigeon_sort(unsorted))
