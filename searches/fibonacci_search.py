"""
斐波那契查找（Fibonacci Search）的纯 Python 实现。

参考资料：
https://en.wikipedia.org/wiki/Fibonacci_search_technique

运行 doctest 请使用以下命令：
python3 -m doctest -v fibonacci_search.py

手动测试请运行：
python3 fibonacci_search.py
"""

from functools import lru_cache


@lru_cache
def fibonacci(k: int) -> int:
    """求索引 k 处的斐波那契数。

    Parameters
    ----------
    k :
        斐波那契数的索引。

    Returns
    -------
    int
        位置 k 处的斐波那契数。

    >>> fibonacci(0)
    0
    >>> fibonacci(2)
    1
    >>> fibonacci(5)
    5
    >>> fibonacci(15)
    610
    >>> fibonacci('a')
    Traceback (most recent call last):
    TypeError: k must be an integer.
    >>> fibonacci(-5)
    Traceback (most recent call last):
    ValueError: k integer must be greater or equal to zero.
    """
    if not isinstance(k, int):
        raise TypeError("k must be an integer.")
    if k < 0:
        raise ValueError("k integer must be greater or equal to zero.")
    if k == 0:
        return 0
    elif k == 1:
        return 1
    else:
        return fibonacci(k - 1) + fibonacci(k - 2)


def fibonacci_search(arr: list, val: int) -> int:
    """斐波那契查找算法的纯 Python 实现。

    Parameters
    ----------
    arr
        已排序的元素列表。
    val
        要在列表中查找的元素。

    Returns
    -------
    int
        元素在数组中的索引。
        未找到元素时返回 -1。

    >>> fibonacci_search([4, 5, 6, 7], 4)
    0
    >>> fibonacci_search([4, 5, 6, 7], -10)
    -1
    >>> fibonacci_search([-18, 2], -18)
    0
    >>> fibonacci_search([5], 5)
    0
    >>> fibonacci_search(['a', 'c', 'd'], 'c')
    1
    >>> fibonacci_search(['a', 'c', 'd'], 'f')
    -1
    >>> fibonacci_search([], 1)
    -1
    >>> fibonacci_search([.1, .4 , 7], .4)
    1
    >>> fibonacci_search([], 9)
    -1
    >>> fibonacci_search(list(range(100)), 63)
    63
    >>> fibonacci_search(list(range(100)), 99)
    99
    >>> fibonacci_search(list(range(-100, 100, 3)), -97)
    1
    >>> fibonacci_search(list(range(-100, 100, 3)), 0)
    -1
    >>> fibonacci_search(list(range(-100, 100, 5)), 0)
    20
    >>> fibonacci_search(list(range(-100, 100, 5)), 95)
    39
    """
    len_list = len(arr)
    # 找到满足 F_m >= n 的 m，其中 F_i 是第 i 个斐波那契数。
    i = 0
    while True:
        if fibonacci(i) >= len_list:
            fibb_k = i
            break
        i += 1
    offset = 0
    while fibb_k > 0:
        index_k = min(
            offset + fibonacci(fibb_k - 1), len_list - 1
        )  # 防止索引越界
        item_k_1 = arr[index_k]
        if item_k_1 == val:
            return index_k
        elif val < item_k_1:
            fibb_k -= 1
        elif val > item_k_1:
            offset += fibonacci(fibb_k - 1)
            fibb_k -= 2
    return -1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
