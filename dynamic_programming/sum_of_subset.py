def is_sum_subset(arr: list[int], required_sum: int) -> bool:
    """
    >>> is_sum_subset([2, 4, 6, 8], 5)
    False
    >>> is_sum_subset([2, 4, 6, 8], 14)
    True
    """
    # 如果可以形成该子集和，则 subset 值为 1，否则为 0
    # 初始时无法形成任何子集，因此为 False/0
    arr_len = len(arr)
    subset = [[False] * (required_sum + 1) for _ in range(arr_len + 1)]

    # 对于每个 arr 值，不取任何元素即可形成和为零(0)的子集，因此为 True/1
    for i in range(arr_len + 1):
        subset[i][0] = True

    # 当和不为零且集合为空时，结果为 false
    for i in range(1, required_sum + 1):
        subset[0][i] = False

    for i in range(1, arr_len + 1):
        for j in range(1, required_sum + 1):
            if arr[i - 1] > j:
                subset[i][j] = subset[i - 1][j]
            if arr[i - 1] <= j:
                subset[i][j] = subset[i - 1][j] or subset[i - 1][j - arr[i - 1]]

    return subset[arr_len][required_sum]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
