"""
荷兰国旗排序（Dutch National Flag，DNF）算法的纯 Python 实现。
荷兰国旗算法最初由 Edsger Dijkstra 设计。
对于仅包含 3 种不同值（如 0、1、2）的序列，它是一种最优排序方法。DNF 可以
在单次遍历中，以保证的 O(n) 复杂度对满足 [0 <= a[i] <= 2] 的
长度为 n 的序列排序。

荷兰国旗由白、红、蓝三色组成。
任务是将随机排列的白、红、蓝球重新排列，使
相同颜色的球聚在一起。DNF 在线性时间内对 0、1、2 的序列排序，
不消耗额外空间。此算法仅适用于
包含三种不同元素的序列。

1) 时间复杂度为 O(n)。
2) 空间复杂度为 O(1)。

More info on: https://en.wikipedia.org/wiki/Dutch_national_flag_problem

运行 doctest 请使用以下命令：
python3 -m doctest -v dutch_national_flag_sort.py

手动测试请运行：
python dnf_sort.py
"""

# 通过单次遍历对仅含 0、1、2 的序列排序的 Python 程序。
red = 0  # 国旗的第一种颜色。
white = 1  # 国旗的第二种颜色。
blue = 2  # 国旗的第三种颜色。
colors = (red, white, blue)


def dutch_national_flag_sort(sequence: list) -> list:
    """
    荷兰国旗排序算法的纯 Python 实现。
    :param data: 包含 3 种不同整数值（如 0、1、2）的序列
    :return: 按升序排列后的同一个集合

    >>> dutch_national_flag_sort([])
    []
    >>> dutch_national_flag_sort([0])
    [0]
    >>> dutch_national_flag_sort([2, 1, 0, 0, 1, 2])
    [0, 0, 1, 1, 2, 2]
    >>> dutch_national_flag_sort([0, 1, 1, 0, 1, 2, 1, 2, 0, 0, 0, 1])
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2]
    >>> dutch_national_flag_sort("abacab")
    Traceback (most recent call last):
      ...
    ValueError: The elements inside the sequence must contains only (0, 1, 2) values
    >>> dutch_national_flag_sort("Abacab")
    Traceback (most recent call last):
      ...
    ValueError: The elements inside the sequence must contains only (0, 1, 2) values
    >>> dutch_national_flag_sort([3, 2, 3, 1, 3, 0, 3])
    Traceback (most recent call last):
      ...
    ValueError: The elements inside the sequence must contains only (0, 1, 2) values
    >>> dutch_national_flag_sort([-1, 2, -1, 1, -1, 0, -1])
    Traceback (most recent call last):
      ...
    ValueError: The elements inside the sequence must contains only (0, 1, 2) values
    >>> dutch_national_flag_sort([1.1, 2, 1.1, 1, 1.1, 0, 1.1])
    Traceback (most recent call last):
      ...
    ValueError: The elements inside the sequence must contains only (0, 1, 2) values
    """
    if not sequence:
        return []
    if len(sequence) == 1:
        return list(sequence)
    low = 0
    high = len(sequence) - 1
    mid = 0
    while mid <= high:
        if sequence[mid] == colors[0]:
            sequence[low], sequence[mid] = sequence[mid], sequence[low]
            low += 1
            mid += 1
        elif sequence[mid] == colors[1]:
            mid += 1
        elif sequence[mid] == colors[2]:
            sequence[mid], sequence[high] = sequence[high], sequence[mid]
            high -= 1
        else:
            msg = f"The elements inside the sequence must contains only {colors} values"
            raise ValueError(msg)
    return sequence


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    user_input = input("Enter numbers separated by commas:\n").strip()
    unsorted = [int(item.strip()) for item in user_input.split(",")]
    print(f"{dutch_national_flag_sort(unsorted)}")
