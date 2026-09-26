"""
使用贪心算法计算最小等待时间。
reference: https://www.youtube.com/watch?v=Sf3eiO12eJs

运行 doctest 请使用以下命令：
python -m doctest -v minimum_waiting_time.py

The minimum_waiting_time function uses a greedy algorithm to calculate the minimum
time for queries to complete. It sorts the list in non-decreasing order, calculates
the waiting time for each query by multiplying its position in the list with the
sum of all remaining query times, and returns the total waiting time. A doctest
ensures that the function produces the correct output.
"""


def minimum_waiting_time(queries: list[int]) -> int:
    """
    接收查询耗时列表，返回完成所有查询所需的
    最小总等待时间。

    Args:
        queries: 查询耗时列表，单位为皮秒

    Returns:
        total_waiting_time: 最小等待时间，单位为皮秒

    示例：
    >>> minimum_waiting_time([3, 2, 1, 2, 6])
    17
    >>> minimum_waiting_time([3, 2, 1])
    4
    >>> minimum_waiting_time([1, 2, 3, 4])
    10
    >>> minimum_waiting_time([5, 5, 5, 5])
    30
    >>> minimum_waiting_time([])
    0
    """
    n = len(queries)
    if n in (0, 1):
        return 0
    return sum(query * (n - i - 1) for i, query in enumerate(sorted(queries)))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
