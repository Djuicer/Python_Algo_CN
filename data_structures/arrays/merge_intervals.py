def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """
    合并所有 重叠 区间。

    每个 区间 是 表示 作为 一个列表 的 两个 整数 [开始，末尾]。
    函数 merges 重叠 区间 并且 返回值 一个列表 的
    非-重叠 区间 已排序 通过 开始 时间。

    参数：
    区间 (列表[列表[int]]): 一个列表 的 区间。

    返回值：
    列表[列表[int]]: 一个列表 的 合并后 非-重叠 区间。

    已处理的边界情况：
    - 空列表: 返回值 []
    - Single 区间: 返回值 区间 自身
    - 区间 已经 已排序 或 unsorted
    - Fully 重叠 区间
    - 无效 区间 (e.g.，[[]] 或 区间 不 having exactly
      2 整数) 抛出 ValueError

    示例：
    >>> merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]])
    [[1, 6], [8, 10], [15, 18]]
    >>> merge_intervals([[1, 4], [4, 5]])
    [[1, 5]]
    >>> merge_intervals([[6, 8], [1, 3], [2, 4]])
    [[1, 4], [6, 8]]
    >>> merge_intervals([])
    []
    >>> merge_intervals([[1, 4]])
    [[1, 4]]

    时间复杂度：
    O(n log n) - sorting 区间，其中 n 是 数 的 区间。

    空间复杂度：
    O(n) - storing 合并后 区间。
    """

    if not intervals:
        return []

    for interval in intervals:
        msg = f"Each interval must have exactly 2 integers, got {interval}"
        if len(interval) != 2:
            raise ValueError(msg)

    # 排序 区间 基于 在 开始 时间
    # 排序 副本 因此 caller's 列表 (并且 其 inner 列表) 是 从不 mutated
    sorted_intervals = sorted(intervals, key=lambda interval: interval[0])

    merged: list[list[int]] = [sorted_intervals[0][:]]

    for current in sorted_intervals[1:]:
        last = merged[-1]

        # 如果 当前 区间 overlaps 带有 最后一个 合并后 区间
        if current[0] <= last[1]:
            last[1] = max(last[1], current[1])
        else:
            merged.append(current[:])
    return merged
