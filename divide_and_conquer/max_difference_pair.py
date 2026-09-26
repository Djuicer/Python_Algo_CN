def max_difference(a: list[int]) -> tuple[int, int]:
    """
    给定整数数组 A[1..n]，其中 n >= 1。要求
    找到一对索引 (i, j)，满足
    1 <= i <= j <= n，且 A[j] - A[i] 尽可能大。

    说明：
    https://www.geeksforgeeks.org/maximum-difference-between-two-elements/

    >>> max_difference([5, 11, 2, 1, 7, 9, 0, 7])
    (1, 9)
    """
    # 递归终止条件
    if len(a) == 1:
        return a[0], a[0]
    else:
        # 将 A 分成两半。
        first = a[: len(a) // 2]
        second = a[len(a) // 2 :]

        # 两个子问题，各自规模为原问题的一半。
        small1, big1 = max_difference(first)
        small2, big2 = max_difference(second)

        # 求前半部分的最小值和后半部分的最大值
        # 线性时间
        min_first = min(first)
        max_second = max(second)

        # 共有 3 种情况：(small1, big1)、
        # (min_first, max_second), (small2, big2)
        # 进行常数次比较
        if big2 - small2 > max_second - min_first and big2 - small2 > big1 - small1:
            return small2, big2
        elif big1 - small1 > max_second - min_first:
            return small1, big1
        else:
            return min_first, max_second


if __name__ == "__main__":
    import doctest

    doctest.testmod()
