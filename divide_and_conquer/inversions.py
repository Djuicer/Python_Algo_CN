"""
给定类数组数据结构 A[1..n]，满足
1 <= i < j <= n 且 A[i] > A[j] 的数对 (i, j) 有多少个？这些数对
称为逆序对（Inversion）。统计类数组对象中的逆序对数量
很重要。例如，统计逆序对可以帮助
判断给定数组距离有序状态有多近。
此处提供两种算法：时间复杂度为 nlogn 的分治算法，
以及时间复杂度为 n^2 的暴力算法。
"""


def count_inversions_bf(arr):
    """
    使用朴素暴力算法统计逆序对数量
    Parameters
    ----------
    arr: arr: 类数组对象，包含待统计逆序对数量的
    元素列表。`arr` 的元素必须可比较。
    Returns
    -------
    num_inversions: `arr` 中的逆序对总数
    Examples
    ---------
     >>> count_inversions_bf([1, 4, 2, 4, 1])
     4
     >>> count_inversions_bf([1, 1, 2, 4, 4])
     0
     >>> count_inversions_bf([])
     0
    """

    num_inversions = 0
    n = len(arr)

    for i in range(n - 1):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                num_inversions += 1

    return num_inversions


def count_inversions_recursive(arr):
    """
    使用分治算法统计逆序对数量
    Parameters
    -----------
    arr: 类数组对象，包含待统计逆序对数量的
    元素列表。`arr` 的元素必须可比较。
    Returns
    -------
    C: `arr` 的已排序副本。
    num_inversions: int，'arr' 中的逆序对总数
    Examples
    --------
    >>> count_inversions_recursive([1, 4, 2, 4, 1])
    ([1, 1, 2, 4, 4], 4)
    >>> count_inversions_recursive([1, 1, 2, 4, 4])
    ([1, 1, 2, 4, 4], 0)
    >>> count_inversions_recursive([])
    ([], 0)
    """
    if len(arr) <= 1:
        return arr, 0
    mid = len(arr) // 2
    p = arr[0:mid]
    q = arr[mid:]

    a, inversion_p = count_inversions_recursive(p)
    b, inversions_q = count_inversions_recursive(q)
    c, cross_inversions = _count_cross_inversions(a, b)

    num_inversions = inversion_p + inversions_q + cross_inversions
    return c, num_inversions


def _count_cross_inversions(p, q):
    """
    统计跨两个有序数组的逆序对。
    并将两个数组合并为一个有序数组
    对于所有 1<= i<=len(P) 和 1 <= j <= len(Q)，
    若 P[i] > Q[j]，则 (i, j) 为跨数组的逆序对
    Parameters
    ----------
    P: 类数组对象，按非递减顺序排列
    Q: 类数组对象，按非递减顺序排列
    Returns
    ------
    R: 类数组对象，由 `P` 和 `Q` 的元素组成的有序数组
    num_inversion: int，跨 `P` 和 `Q` 的逆序对数量
    Examples
    --------
    >>> _count_cross_inversions([1, 2, 3], [0, 2, 5])
    ([0, 1, 2, 2, 3, 5], 4)
    >>> _count_cross_inversions([1, 2, 3], [3, 4, 5])
    ([1, 2, 3, 3, 4, 5], 0)
    """

    r = []
    i = j = num_inversion = 0
    while i < len(p) and j < len(q):
        if p[i] > q[j]:
            # if P[1] > Q[j], then P[k] > Q[k] for all  i < k <= len(P)
            # These are all inversions. The claim emerges from the
            # property that P is sorted.
            num_inversion += len(p) - i
            r.append(q[j])
            j += 1
        else:
            r.append(p[i])
            i += 1

    if i < len(p):
        r.extend(p[i:])
    else:
        r.extend(q[j:])

    return r, num_inversion


def main() -> None:
    arr_1 = [10, 2, 1, 5, 5, 2, 11]

    # 此 arr 中有 8 个逆序对：
    # (10, 2), (10, 1), (10, 5), (10, 5), (10, 2), (2, 1), (5, 2), (5, 2)

    num_inversions_bf = count_inversions_bf(arr_1)
    _, num_inversions_recursive = count_inversions_recursive(arr_1)

    assert num_inversions_bf == num_inversions_recursive == 8

    print("number of inversions = ", num_inversions_bf)

    # 测试没有逆序对的数组（已排序的 arr_1）

    arr_1.sort()
    num_inversions_bf = count_inversions_bf(arr_1)
    _, num_inversions_recursive = count_inversions_recursive(arr_1)

    assert num_inversions_bf == num_inversions_recursive == 0
    print("number of inversions = ", num_inversions_bf)

    # 空列表的逆序对数量也应为零
    arr_1 = []
    num_inversions_bf = count_inversions_bf(arr_1)
    _, num_inversions_recursive = count_inversions_recursive(arr_1)

    assert num_inversions_bf == num_inversions_recursive == 0
    print("number of inversions = ", num_inversions_bf)


if __name__ == "__main__":
    main()
