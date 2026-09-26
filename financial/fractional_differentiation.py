"""实现 Marcos Lopez de Prado 所著 `Advances in Financial Machine Learning` 一书中的
分数阶差分。

分数阶差分是一种在保留原始数据记忆性的同时使时间序列平稳化的技术。

此实现使用固定窗口大小计算分数阶差分。与 Marcos Lopez de Prado 书中介绍的方法
相比，这是一个简化版本，不考虑权重损失。书中计算权重损失，是为了考虑序列
起始数据点与末尾数据点所含信息量不同这一事实。

计算分数阶差分时，将价格与权重进行卷积以获得分数阶差分序列。该过程可在保留
原始数据记忆性的同时，将时间序列转换为平稳形式。

为确定最佳差分阶数，需要在 0 到 1 之间找到可使时间序列平稳的最小差分阶数。

参考资料
---------
https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086

https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3257419

"""

from collections.abc import Sequence
from math import nan


def calculate_weights(degree: float, length: int) -> list[float]:
    r"""计算分数阶差分的权重。

    .. math::

        w_{0} = 1
        w_{k} = -w_{k-1} * (d - k + 1) / k

    参数
    ----------
    degree : float
        差分阶数。
    length : int
        权重长度。

    返回值
    -------
    list[float]
        分数阶差分的权重。

    示例
    --------
    >>> calculate_weights(0.5, 3)
    [1.0, -0.5, -0.125]
    >>> calculate_weights(0.5, 4)
    [1.0, -0.5, -0.125, -0.0625]
    """
    weights = [1.0]
    for k in range(1, length):
        weights.append(-1 * weights[-1] * (degree - k + 1) / k)
    return weights


def fracdiff_fixedwindow(
    price_series: Sequence[float], degree: float, window_size: int
) -> list[float]:
    """使用固定窗口大小计算分数阶差分。

    参数
    ----------
    price_series : Sequence[float]
        用于计算分数阶差分的价格序列。
    degree : float
        差分阶数。
    window_size : int
        计算每个值时使用的历史观测值数量。

    返回值
    -------
    list[float]
        分数阶差分序列。

    异常
    ------
    ValueError
        当 ``window_size`` 大于 ``price_series`` 的长度时引发。

    示例
    --------
    >>> price_series = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> fracdiff_fixedwindow(price_series, 0.5, 3)
    [nan, nan, nan, 2.25, 2.625, 3.0, 3.375, 3.75, 4.125, 4.5]
    """
    if window_size > len(price_series):
        raise ValueError("window_size cannot exceed the length of price_series")
    weights = calculate_weights(degree=degree, length=window_size)
    frac_diff_series = [nan] * window_size
    for i in range(window_size, len(price_series)):
        frac_diff_series.append(
            sum(weights[j] * price_series[i - j] for j in range(window_size))
        )
    return frac_diff_series


if __name__ == "__main__":
    import doctest

    doctest.testmod()
