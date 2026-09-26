"""
用于衡量投资组合风险调整后收益的夏普比率（Sharpe Ratio）。

夏普比率是诺贝尔奖得主 William F. Sharpe 提出的风险调整后收益指标。它计算每单位
风险（标准差）对应的超额收益，广泛用于比较投资组合的表现。

维基百科参考资料：https://en.wikipedia.org/wiki/Sharpe_ratio
Investopedia: https://www.investopedia.com/terms/s/sharperatio.asp

夏普比率用于：
- 比较不同投资策略的表现
- 评估共同基金和对冲基金
- 投资组合优化和风险管理
- 评估交易策略的风险调整后收益
"""

from __future__ import annotations


def sharpe_ratio(returns: list[float], risk_free_rate: float = 0.0) -> float:
    """
    计算一系列收益率的夏普比率。

    夏普比率公式：
    S = (R - Rf) / std_dev

    其中：
    S = 夏普比率
    R = 投资的平均收益率
    Rf = 无风险收益率
    std_dev = 收益率的标准差（波动率）

    :param returns: 周期收益率列表（例如日收益率、月收益率）
    :param risk_free_rate: 每期无风险收益率，默认为 0.0
    :return: 夏普比率

    >>> round(sharpe_ratio([0.1, 0.2, 0.15, 0.05, 0.12]), 4)
    2.2164
    >>> sharpe_ratio([0.05, 0.05, 0.05, 0.05, 0.05])
    inf
    >>> round(sharpe_ratio([0.1, 0.2, 0.15, 0.05, 0.12], 0.02), 4)
    1.8589
    >>> sharpe_ratio([0.0, 0.0, 0.0, 0.0, 0.0])
    0.0
    >>> round(sharpe_ratio([-0.05, -0.1, -0.08, -0.12, -0.15]), 4)
    -2.6261
    >>> sharpe_ratio([])
    Traceback (most recent call last):
        ...
    ValueError: returns list must not be empty
    >>> sharpe_ratio([0.1])
    Traceback (most recent call last):
        ...
    ValueError: returns list must contain at least 2 values
    """
    if not returns:
        raise ValueError("returns list must not be empty")
    if len(returns) < 2:
        raise ValueError("returns list must contain at least 2 values")

    # 计算平均收益率
    mean_return = sum(returns) / len(returns)

    # 计算超额收益率
    excess_return = mean_return - risk_free_rate

    # 计算标准差（使用分母为 n-1 的样本标准差）
    variance = sum((r - mean_return) ** 2 for r in returns) / (len(returns) - 1)
    std_dev = variance**0.5

    # 处理波动率为零的情形
    if std_dev == 0:
        return float("inf") if excess_return > 0 else 0.0

    return excess_return / std_dev


def annualized_sharpe_ratio(
    returns: list[float], risk_free_rate: float = 0.0, periods_per_year: int = 252
) -> float:
    """
    计算一系列周期收益率的年化夏普比率。

    年化夏普比率考虑收益率的时间周期：
    S_annual = S_periodic * sqrt(periods_per_year)

    常用 periods_per_year 值：
    - 日收益率：252（交易日）
    - 周收益率：52
    - 月收益率：12
    - 季度收益率：4

    :param returns: 周期收益率列表
    :param risk_free_rate: 每期无风险收益率，默认为 0.0
    :param periods_per_year: 每年的周期数，默认为 252（日频）
    :return: 年化夏普比率

    >>> round(annualized_sharpe_ratio(
    ...     [0.001, 0.002, 0.0015, 0.0005, 0.0012], 0.0, 252), 4)
    35.1844
    >>> round(annualized_sharpe_ratio([0.01, 0.02, 0.015, 0.005, 0.012], 0.0, 12), 4)
    7.6779
    >>> round(annualized_sharpe_ratio([0.05, 0.06, 0.055, 0.045, 0.052], 0.0, 4), 4)
    18.7322
    >>> round(annualized_sharpe_ratio([0.001, 0.002, 0.0015], 0.0001, 252), 4)
    44.4486
    >>> round(annualized_sharpe_ratio([0.001, 0.002], 0.0, 252), 4)
    33.6749
    >>> annualized_sharpe_ratio([0.001, 0.002, 0.0015], 0.0, 0)
    Traceback (most recent call last):
        ...
    ValueError: periods_per_year must be > 0
    >>> annualized_sharpe_ratio([0.001, 0.002, 0.0015], 0.0, -252)
    Traceback (most recent call last):
        ...
    ValueError: periods_per_year must be > 0
    """
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be > 0")

    periodic_sharpe = sharpe_ratio(returns, risk_free_rate)

    # 乘以周期数的平方根进行年化
    if periodic_sharpe == float("inf"):
        return float("inf")

    return periodic_sharpe * (periods_per_year**0.5)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # 示例：计算一系列月收益率的夏普比率
    monthly_returns = [0.02, 0.03, -0.01, 0.04, 0.01, 0.02, -0.02, 0.03, 0.02, 0.01]
    risk_free = 0.002  # 月无风险利率为 0.2%

    sharpe = sharpe_ratio(monthly_returns, risk_free)
    annualized = annualized_sharpe_ratio(monthly_returns, risk_free, 12)

    print(f"Monthly returns: {monthly_returns}")
    print(f"Risk-free rate: {risk_free:.2%}")
    print(f"Sharpe Ratio: {sharpe:.4f}")
    print(f"Annualized Sharpe Ratio: {annualized:.4f}")
