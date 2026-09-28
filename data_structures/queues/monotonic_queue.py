from __future__ import annotations

from collections import deque

arr = [1, 3, -1, -3, 5, 3, 6, 7]
window_size = 3
expect = [3, 3, 5, 5, 6, 7]


def max_sliding_window(arr: list[float], window_size: int) -> list[float]:
    """
    给定一个数组 的 整数 nums，其中 是 sliding window 的 大小 k 其 是 moving
    从 very 左 的数组 到 very 右。
    每个 时间 sliding window 的 长度 window_size 移动 右 通过 一个 位置。
    返回 最大值 sliding window。
    >>> max_sliding_window(arr, window_size) == expect
    True
    """
    max_val = []
    mono_queue: deque = deque()
    for i in range(len(arr)):
        # 弹出 元素 如果 该索引 是 outside window 大小 k
        if mono_queue and i - mono_queue[0] >= window_size:
            mono_queue.popleft()
        # 保持 该队列 monotonically decreasing
        # 因此 该 最大值 值 是 始终 在 顶部
        while mono_queue and arr[i] >= arr[mono_queue[-1]]:
            mono_queue.pop()
        mono_queue.append(i)
        # 最大值 值 是 第一个元素 在 队列
        if i >= window_size - 1:
            max_val.append(arr[mono_queue[0]])
    return max_val


if __name__ == "__main__":
    from doctest import testmod

    testmod()
