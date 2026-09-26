"""
使用历史模拟法计算风险价值（Value at Risk, VaR）。

参考资料：
- https://en.wikipedia.org/wiki/Value_at_risk
- https://www.investopedia.com/terms/v/var.asp

风险价值衡量投资组合在给定期间和选定置信水平下可能遭受的最大损失。历史模拟是
一种非参数方法：它重复使用观测收益率并从经验分布中读取分位数，因此不对损失
分布的形状作任何假设。结果为相应收益率分位数的相反数；当分布尾部包含损失时，
结果为正的损失幅度。
"""

from collections.abc import Sequence
from math import isfinite


def _linear_interpolated_quantile(
    sorted_values: Sequence[float], quantile: float
) -> float:
    """
    在最接近的秩之间进行线性插值（NumPy 默认方法，type 7）。

    >>> _linear_interpolated_quantile([-10.0, -5.0, -2.0, 1.0, 4.0], 0.05)
    -9.0
    >>> _linear_interpolated_quantile([1.0, 2.0, 3.0], 1.0)
    3.0
    """
    position = (len(sorted_values) - 1) * quantile
    lower_index = int(position)
    fraction = position - lower_index
    if lower_index == len(sorted_values) - 1:
        return sorted_values[-1]
    return sorted_values[lower_index] * (1 - fraction) + (
        sorted_values[lower_index + 1] * fraction
    )


def value_at_risk(returns: Sequence[float], confidence_level: float = 0.95) -> float:
    """
    计算投资组合基于历史模拟的风险价值。

    置信水平表示损失不超过返回值的概率。默认值 0.95 表示 95% 的观测收益率优于
    （高于）VaR 阈值，其余 5% 更差。

    示例：
    >>> value_at_risk([-10, -5, -2, 1, 4], 0.95)
    9.0
    >>> value_at_risk([-2, -1, 0, 1, 2, 3], 0.90)
    1.5
    >>> value_at_risk([5, 10, 15], 0.75)
    -7.5
    >>> value_at_risk([], 0.95)
    Traceback (most recent call last):
    ...
    ValueError: returns must not be empty
    >>> value_at_risk([-1, 0, 1], 1.0)
    Traceback (most recent call last):
    ...
    ValueError: confidence_level must be strictly between 0 and 1
    >>> value_at_risk([-1, float("nan"), 1], 0.95)
    Traceback (most recent call last):
    ...
    ValueError: returns must contain only finite numbers

    时间复杂度：排序需要 O(n log n)，其中 n = len(returns)。
    空间复杂度：有序副本需要 O(n)。
    """
    if not returns:
        raise ValueError("returns must not be empty")
    if not all(isfinite(value) for value in returns):
        raise ValueError("returns must contain only finite numbers")
    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level must be strictly between 0 and 1")

    sorted_returns = sorted(returns)
    threshold = _linear_interpolated_quantile(sorted_returns, 1 - confidence_level)
    return -threshold


if __name__ == "__main__":
    import doctest

    doctest.testmod()
