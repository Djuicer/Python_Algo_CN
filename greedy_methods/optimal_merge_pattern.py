"""
贪心归并排序算法的纯 Python 实现
参考资料：https://www.geeksforgeeks.org/optimal-file-merge-patterns/

运行 doctest 请使用以下命令：
python3 -m doctest -v greedy_merge_sort.py

目标
将一组长度不同的有序文件合并为一个有序文件。
需要找到最优方案，
以最短时间生成结果文件。

思路
给定多个有序文件时，有多种方式
可以将它们合并为一个有序文件。
可以采用两两合并的方式。
合并包含 m 条和 n 条记录的文件，可能需要移动 m+n 条记录，
最优的选择是：
每一步都合并最小的两个文件（贪心策略）。
"""


def optimal_merge_pattern(files: list) -> float:
    """以最优代价合并所有文件

    参数：
        files [list]：待合并的各文件大小组成的列表

    返回：
        optimal_merge_cost [int]：合并所有文件的最优代价

    示例：
    >>> optimal_merge_pattern([2, 3, 4])
    14
    >>> optimal_merge_pattern([5, 10, 20, 30, 30])
    205
    >>> optimal_merge_pattern([8, 8, 8, 8, 8])
    96
    """
    optimal_merge_cost = 0
    while len(files) > 1:
        temp = 0
        # 考虑合并代价最小的两个文件
        for _ in range(2):
            min_index = files.index(min(files))
            temp += files[min_index]
            files.pop(min_index)
        files.append(temp)
        optimal_merge_cost += temp
    return optimal_merge_cost


if __name__ == "__main__":
    import doctest

    doctest.testmod()
