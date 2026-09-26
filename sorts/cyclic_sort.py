"""
循环排序（Cyclic Sort）算法的纯 Python 实现。

运行 doctest 请使用以下命令：
python -m doctest -v cyclic_sort.py
或
python3 -m doctest -v cyclic_sort.py

手动测试请运行：
python cyclic_sort.py
或
python3 cyclic_sort.py
"""


def cyclic_sort(nums: list[int]) -> list[int]:
    """
    使用循环排序算法，对由 1 到 n 的 n 个整数
    组成的输入列表进行原地排序。

    :param nums: 待排序的列表，包含 1 到 n 的 n 个整数。
    :return: 按升序排列后的同一个列表。

    时间复杂度：O(n)，其中 n 为列表中的整数数量。

    示例：
    >>> cyclic_sort([])
    []
    >>> cyclic_sort([3, 5, 2, 1, 4])
    [1, 2, 3, 4, 5]

    >>> cyclic_sort([1, 2, 2])
    Traceback (most recent call last):
    ...
    ValueError: All numbers must be unique, got 2

    >>> cyclic_sort([1, 5])
    Traceback (most recent call last):
    ...
    ValueError: All numbers must be in range 1 to 2, got 5
    """

    # 验证输入
    seen = set()
    n = len(nums)

    for num in nums:
        if num in seen:
            message = f"All numbers must be unique, got {num}"
            raise ValueError(message)

        if num < 1 or num > n:
            message = f"All numbers must be in range 1 to {n}, got {num}"
            raise ValueError(message)

        seen.add(num)

    # 执行循环排序
    index = 0
    while index < len(nums):
        correct_index = nums[index] - 1

        if index != correct_index:
            nums[index], nums[correct_index] = nums[correct_index], nums[index]

        else:
            index += 1

    return nums


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    print(*cyclic_sort(unsorted), sep=",")
