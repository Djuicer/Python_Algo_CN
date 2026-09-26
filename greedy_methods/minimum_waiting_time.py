"""
使用贪心算法计算最小等待时间。
参考资料：https://www.youtube.com/watch?v=Sf3eiO12eJs

运行 doctest 请使用以下命令：
python -m doctest -v minimum_waiting_time.py

minimum_waiting_time 函数使用贪心算法计算完成查询所需的最短时间。它将列表按
非递减顺序排序，根据每个查询在列表中的位置和剩余查询时间计算等待时间，
并返回总等待时间。doctest 用于验证函数能否生成正确输出。
"""


def minimum_waiting_time(queries: list[int]) -> int:
    """
    接收查询耗时列表，返回完成所有查询所需的
    最小总等待时间。

    参数：
        queries：查询耗时列表，单位为皮秒

    返回：
        total_waiting_time：最小等待时间，单位为皮秒

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
