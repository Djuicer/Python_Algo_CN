"""
计算股票价格序列的指数移动平均值（EMA）。
维基百科参考资料：https://en.wikipedia.org/wiki/Exponential_smoothing
https://www.investopedia.com/terms/e/ema.asp#toc-what-is-an-exponential
-moving-average-ema

指数移动平均值在金融领域用于分析股票价格变化。EMA 常与简单移动平均值（SMA）
配合使用；EMA 对数值变化的反应比 SMA 更快，这是使用 EMA 的优势之一。
"""

from collections.abc import Iterator


def exponential_moving_average(
    stock_prices: Iterator[float], window_size: int
) -> Iterator[float]:
    """
    逐个生成给定股票价格的指数移动平均值。
    >>> tuple(exponential_moving_average(iter([2, 5, 3, 8.2, 6, 9, 10]), 3))
    (2, 3.5, 3.25, 5.725, 5.8625, 7.43125, 8.715625)

    :param stock_prices: 股票价格流
    :param window_size: 触发一次新指数平均值计算所需的股票价格数量
                        （window_size > 0）
    :return: 逐个生成指数移动平均值序列

    公式：

    st = alpha * xt + (1 - alpha) * st_prev

    其中：
    st : 时间戳 t 处的指数移动平均值
    xt : 时间戳 t 处的股票价格
    st_prev : 时间戳 t-1 处的指数移动平均值
    alpha : 2/(1 + window_size) - 平滑因子

    指数移动平均值（EMA）是一种使用指数窗口函数平滑时间序列数据的经验方法。
    """

    if window_size <= 0:
        raise ValueError("window_size must be > 0")

    # 计算平滑因子
    alpha = 2 / (1 + window_size)

        # 时间戳 t 处的指数平均值
    moving_average = 0.0

    for i, stock_price in enumerate(stock_prices):
        if i <= window_size:
            # 首次达到 window_size 前使用简单移动平均值
            moving_average = (moving_average + stock_price) * 0.5 if i else stock_price
        else:
            # 根据当前时间戳的数据点和前一个指数平均值计算指数移动平均值
            moving_average = (alpha * stock_price) + ((1 - alpha) * moving_average)
        yield moving_average


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    stock_prices = [2.0, 5, 3, 8.2, 6, 9, 10]
    window_size = 3
    result = tuple(exponential_moving_average(iter(stock_prices), window_size))
    print(f"{stock_prices = }")
    print(f"{window_size = }")
    print(f"{result = }")
