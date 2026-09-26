"""
线性查找（Linear Search）算法的纯 Python 实现。

运行 doctest 请使用以下命令：
python3 -m doctest -v linear_search.py

手动测试请运行：
python3 linear_search.py
"""


def linear_search(sequence: list, target: int) -> int:
    """线性查找算法的纯 Python 实现

    :param sequence: 元素可比较的集合（线性查找
        不要求排序）
    :param target: 待查找的元素值
    :return: 找到的元素索引；未找到则返回 -1

    示例：
    >>> linear_search([0, 5, 7, 10, 15], 0)
    0
    >>> linear_search([0, 5, 7, 10, 15], 15)
    4
    >>> linear_search([0, 5, 7, 10, 15], 5)
    1
    >>> linear_search([0, 5, 7, 10, 15], 6)
    -1
    """
    for index, item in enumerate(sequence):
        if item == target:
            return index
    return -1


def rec_linear_search(sequence: list, low: int, high: int, target: int) -> int:
    """
    线性查找算法的纯 Python 递归实现

    :param sequence: 元素可比较的集合（线性查找
        不要求排序）
    :param low: 数组的下界
    :param high: 数组的上界
    :param target: 待查找的元素
    :return: 键值的索引；未找到则返回 -1

    示例：
    >>> rec_linear_search([0, 30, 500, 100, 700], 0, 4, 0)
    0
    >>> rec_linear_search([0, 30, 500, 100, 700], 0, 4, 700)
    4
    >>> rec_linear_search([0, 30, 500, 100, 700], 0, 4, 30)
    1
    >>> rec_linear_search([0, 30, 500, 100, 700], 0, 4, -6)
    -1
    """
    if not (0 <= high < len(sequence) and 0 <= low < len(sequence)):
        raise ValueError("Invalid upper or lower bound!")
    if high < low:
        return -1
    if sequence[low] == target:
        return low
    if sequence[high] == target:
        return high
    return rec_linear_search(sequence, low + 1, high - 1, target)


if __name__ == "__main__":
    user_input = input("Enter numbers separated by comma:\n").strip()
    sequence = [int(item.strip()) for item in user_input.split(",")]

    target = int(input("Enter a single number to be found in the list:\n").strip())
    result = linear_search(sequence, target)
    if result != -1:
        print(f"linear_search({sequence}, {target}) = {result}")
    else:
        print(f"{target} was not found in {sequence}")
