from __future__ import annotations


def largest_divisible_subset(items: list[int]) -> list[int]:
    """
    寻找给定数组中最大子集的算法，使子集中的任意 2 个元素 x 和 y，
    都满足 x 整除 y 或 y 整除 x。
    >>> largest_divisible_subset([1, 16, 7, 8, 4])
    [16, 8, 4, 1]
    >>> largest_divisible_subset([1, 2, 3])
    [2, 1]
    >>> largest_divisible_subset([-1, -2, -3])
    [-3]
    >>> largest_divisible_subset([1, 2, 4, 8])
    [8, 4, 2, 1]
    >>> largest_divisible_subset((1, 2, 4, 8))
    [8, 4, 2, 1]
    >>> largest_divisible_subset([1, 1, 1])
    [1, 1, 1]
    >>> largest_divisible_subset([0, 0, 0])
    [0, 0, 0]
    >>> largest_divisible_subset([-1, -1, -1])
    [-1, -1, -1]
    >>> largest_divisible_subset([])
    []
    """
    # 由于顺序并不重要，只需选出一个子集，因此将数组按升序排序
    items = sorted(items)

    number_of_items = len(items)

    # 使用 1 初始化 memo，使用递增数字初始化 hash
    memo = [1] * number_of_items
    hash_array = list(range(number_of_items))

    # 遍历数组
    for i, item in enumerate(items):
        for prev_index in range(i):
            if ((items[prev_index] != 0 and item % items[prev_index]) == 0) and (
                (1 + memo[prev_index]) > memo[i]
            ):
                memo[i] = 1 + memo[prev_index]
                hash_array[i] = prev_index

    ans = -1
    last_index = -1

    # 查找最大长度及其对应索引
    for i, memo_item in enumerate(memo):
        if memo_item > ans:
            ans = memo_item
            last_index = i

    # 重建整除子集
    if last_index == -1:
        return []
    result = [items[last_index]]
    while hash_array[last_index] != last_index:
        last_index = hash_array[last_index]
        result.append(items[last_index])

    return result


if __name__ == "__main__":
    from doctest import testmod

    testmod()

    items = [1, 16, 7, 8, 4]
    print(
        f"The longest divisible subset of {items} is {largest_divisible_subset(items)}."
    )
