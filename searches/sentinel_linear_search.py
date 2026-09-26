"""
哨兵线性查找（Sentinel Linear Search）算法的纯 Python 实现

运行 doctest 请使用以下命令：
python -m doctest -v sentinel_linear_search.py
或
python3 -m doctest -v sentinel_linear_search.py

手动测试请运行：
python sentinel_linear_search.py
"""


def sentinel_linear_search(sequence, target):
    """哨兵线性查找算法的纯 Python 实现

    :param sequence: 元素可比较的序列
    :param target: 待查找的元素值
    :return: 找到的元素索引；未找到则返回 None

    示例：
    >>> sentinel_linear_search([0, 5, 7, 10, 15], 0)
    0

    >>> sentinel_linear_search([0, 5, 7, 10, 15], 15)
    4

    >>> sentinel_linear_search([0, 5, 7, 10, 15], 5)
    1

    >>> sentinel_linear_search([0, 5, 7, 10, 15], 6)

    """
    sequence.append(target)

    index = 0
    while sequence[index] != target:
        index += 1

    sequence.pop()

    if index == len(sequence):
        return None

    return index


if __name__ == "__main__":
    user_input = input("Enter numbers separated by comma:\n").strip()
    sequence = [int(item) for item in user_input.split(",")]

    target_input = input("Enter a single number to be found in the list:\n")
    target = int(target_input)
    result = sentinel_linear_search(sequence, target)
    if result is not None:
        print(f"{target} found at positions: {result}")
    else:
        print("Not found")
