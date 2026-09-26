"""
使用历史模拟法估算预期损失（Expected Shortfall, ES），又称条件风险价值（CVaR）。

参考资料：
- https://en.wikipedia.org/wiki/Expected_shortfall
- https://www.investopedia.com/terms/c/conditional_value_at_risk.asp

预期损失衡量损失分布尾部超过风险价值阈值部分的平均损失。风险价值仅报告分位数
边界，而预期损失能反映最坏情形发生时的实际损失程度，并且是一致性风险度量。
"""

from collections.abc import Sequence
from math import isfinite


def _linear_interpolated_quantile(
    sorted_values: Sequence[float], quantile: float
) -> float:
    """
    在最接近的秩之间进行线性插值（NumPy 默认方法，type 7）。

    >>> _linear_interpolated_quantile([-10.0, -5.0, -2.0, 1.0, 4.0], 0.25)
    -5.0
    """
    position = (len(sorted_values) - 1) * quantile
    lower_index = int(position)
    fraction = position - lower_index
    if lower_index == len(sorted_values) - 1:
        return sorted_values[-1]
    return sorted_values[lower_index] * (1 - fraction) + (
        sorted_values[lower_index + 1] * fraction
    )


def expected_shortfall(
    returns: Sequence[float], confidence_level: float = 0.95
) -> float:
    """
    计算投资组合基于历史模拟的预期损失。

    置信水平表示损失不超过相应风险价值阈值的概率。尾部包含所有小于或等于该阈值
    的观测收益率，结果为该尾部平均值的相反数；当尾部包含损失时，结果为正的
    损失幅度。

    示例：
    >>> expected_shortfall([-10, -5, -2, 1, 4], 0.95)
    10.0
    >>> expected_shortfall([-10, -5, -2, 1, 4], 0.75)
    7.5
    >>> expected_shortfall([], 0.95)
    Traceback (most recent call last):
    ...
    ValueError: returns must not be empty
    >>> expected_shortfall([-1, 0, 1], 0.0)
    Traceback (most recent call last):
    ...
    ValueError: confidence_level must be strictly between 0 and 1
    >>> expected_shortfall([-1, float("inf"), 1], 0.95)
    Traceback (most recent call last):
    ...
    ValueError: returns must contain only finite numbers

    时间复杂度：排序需要 O(n log n)，其中 n = len(returns)。
    空间复杂度：有序副本和尾部数据需要 O(n)。
    """
    if not returns:
        raise ValueError("returns must not be empty")
    if not all(isfinite(value) for value in returns):
        raise ValueError("returns must contain only finite numbers")
    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level must be strictly between 0 and 1")

    sorted_returns = sorted(returns)
    threshold = _linear_interpolated_quantile(sorted_returns, 1 - confidence_level)
    tail = [value for value in sorted_returns if value <= threshold]
    return -sum(tail) / len(tail)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
