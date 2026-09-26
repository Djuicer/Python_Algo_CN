"""
简单移动平均值（SMA）是一种统计计算方法，通过创建指定时间段内持续更新的平均
价格来分析数据点。在金融领域，SMA 常用于时间序列分析，以平滑价格数据并识别趋势。

参考资料：https://en.wikipedia.org/wiki/Moving_average
"""

from collections.abc import Sequence


def simple_moving_average(
    data: Sequence[float], window_size: int
) -> list[float | None]:
    """
    计算给定时间序列数据的简单移动平均值（SMA）。

    :param data: 数值数据点列表。
    :param window_size: 表示 SMA 窗口大小的整数。
    :return: 与输入数据长度相同的 SMA 值列表。

    示例：
    >>> sma = simple_moving_average([10, 12, 15, 13, 14, 16, 18, 17, 19, 21], 3)
    >>> [round(value, 2) if value is not None else None for value in sma]
    [None, None, 12.33, 13.33, 14.0, 14.33, 16.0, 17.0, 18.0, 19.0]
    >>> simple_moving_average([10, 12, 15], 5)
    [None, None, None]
    >>> simple_moving_average([10, 12, 15, 13, 14, 16, 18, 17, 19, 21], 0)
    Traceback (most recent call last):
    ...
    ValueError: Window size must be a positive integer
    """
    if window_size < 1:
        raise ValueError("Window size must be a positive integer")

    sma: list[float | None] = []

    for i in range(len(data)):
        if i < window_size - 1:
            sma.append(None)  # 初始数据点尚无法计算 SMA
        else:
            window = data[i - window_size + 1 : i + 1]
            sma_value = sum(window) / window_size
            sma.append(sma_value)
    return sma


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # 示例数据（可替换为自己的时间序列数据）
    data = [10, 12, 15, 13, 14, 16, 18, 17, 19, 21]

    # 指定 SMA 的窗口大小
    window_size = 3

    # 计算简单移动平均值
    sma_values = simple_moving_average(data, window_size)

    # 输出 SMA 值
    print("Simple Moving Average (SMA) Values:")
    for i, value in enumerate(sma_values):
        if value is not None:
            print(f"Day {i + 1}: {value:.2f}")
        else:
            print(f"Day {i + 1}: Not enough data for SMA")
