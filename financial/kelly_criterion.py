"""
用于确定投注和交易最优头寸规模的凯利准则（Kelly Criterion）。

凯利准则用于确定一系列投注或投资的最优规模，以最大化长期对数财富。该公式由
John L. Kelly Jr. 于 1956 年提出。

维基百科参考资料：https://en.wikipedia.org/wiki/Kelly_criterion
Investopedia: https://www.investopedia.com/articles/trading/04/091504.asp

凯利准则广泛用于：
- 在体育博彩和赌博中确定最优投注规模
- 在投资组合管理中确定头寸规模
- 在交易策略中管理风险并最大化增长
"""

from __future__ import annotations


def kelly_criterion(win_probability: float, win_loss_ratio: float) -> float:
    """
    使用凯利准则计算应投注资金的最优比例。

    凯利准则公式：
    f* = (p * b - q) / b

    其中：
    f* = 投注资金比例（凯利比例）
    p = 获胜概率
    q = 失败概率（1 - p）
    b = 盈亏比（每单位投注的赢得金额 / 每单位投注的损失金额）

    :param win_probability: 获胜概率（0 < p < 1）
    :param win_loss_ratio: 赢得金额与损失金额之比（b > 0）
    :return: 应投注资金的最优比例

    >>> round(kelly_criterion(0.6, 2.0), 4)
    0.4
    >>> round(kelly_criterion(0.55, 1.0), 4)
    0.1
    >>> kelly_criterion(0.5, 1.0)
    0.0
    >>> round(kelly_criterion(0.7, 3.0), 4)
    0.6
    >>> round(kelly_criterion(0.3, 2.0), 4)
    -0.05
    >>> kelly_criterion(0.0, 1.0)
    Traceback (most recent call last):
        ...
    ValueError: win_probability must be between 0 and 1 (exclusive)
    >>> kelly_criterion(1.0, 1.0)
    Traceback (most recent call last):
        ...
    ValueError: win_probability must be between 0 and 1 (exclusive)
    >>> kelly_criterion(0.5, 0.0)
    Traceback (most recent call last):
        ...
    ValueError: win_loss_ratio must be > 0
    >>> kelly_criterion(0.5, -1.0)
    Traceback (most recent call last):
        ...
    ValueError: win_loss_ratio must be > 0
    """
    if win_probability <= 0 or win_probability >= 1:
        raise ValueError("win_probability must be between 0 and 1 (exclusive)")
    if win_loss_ratio <= 0:
        raise ValueError("win_loss_ratio must be > 0")

    loss_probability = 1 - win_probability
    kelly_fraction = (win_probability * win_loss_ratio - loss_probability) / (
        win_loss_ratio
    )

    return kelly_fraction


def kelly_criterion_extended(
    win_probability: float, win_amount: float, loss_amount: float
) -> float:
    """
    使用明确的赢得金额和损失金额计算凯利比例。

    这是凯利准则更一般的形式，接受绝对赢得金额和损失金额，而非两者的比率。

    公式：
    f* = (p * W - q * L) / (W * L)

    其中：
    p = 获胜概率
    q = 失败概率（1 - p）
    W = 每单位投注的赢得金额
    L = 每单位投注的损失金额（正值）

    :param win_probability: 获胜概率（0 < p < 1）
    :param win_amount: 每单位投注的赢得金额（W > 0）
    :param loss_amount: 每单位投注的损失金额（L > 0）
    :return: 应投注资金的最优比例

    >>> round(kelly_criterion_extended(0.6, 2.0, 1.0), 4)
    0.4
    >>> round(kelly_criterion_extended(0.55, 1.5, 1.5), 4)
    0.1
    >>> kelly_criterion_extended(0.5, 1.0, 1.0)
    0.0
    >>> round(kelly_criterion_extended(0.7, 3.0, 1.0), 4)
    0.6
    >>> kelly_criterion_extended(0.0, 1.0, 1.0)
    Traceback (most recent call last):
        ...
    ValueError: win_probability must be between 0 and 1 (exclusive)
    >>> kelly_criterion_extended(0.5, 0.0, 1.0)
    Traceback (most recent call last):
        ...
    ValueError: win_amount must be > 0
    >>> kelly_criterion_extended(0.5, 1.0, 0.0)
    Traceback (most recent call last):
        ...
    ValueError: loss_amount must be > 0
    """
    if win_probability <= 0 or win_probability >= 1:
        raise ValueError("win_probability must be between 0 and 1 (exclusive)")
    if win_amount <= 0:
        raise ValueError("win_amount must be > 0")
    if loss_amount <= 0:
        raise ValueError("loss_amount must be > 0")

    loss_probability = 1 - win_probability
    # 转换为盈亏比形式：b = win_amount / loss_amount
    # 然后应用凯利公式：(p * b - q) / b
    win_loss_ratio = win_amount / loss_amount
    kelly_fraction = (win_probability * win_loss_ratio - loss_probability) / (
        win_loss_ratio
    )

    return kelly_fraction


def fractional_kelly(
    win_probability: float, win_loss_ratio: float, fraction: float = 0.5
) -> float:
    """
    计算分数凯利投注规模以降低波动性。

    许多实践者使用凯利比例的一部分（例如半凯利），在保持良好增长的同时降低风险
    和波动性，因为完整凯利策略可能导致较大回撤。

    公式：
    f*_fractional = fraction * f*

    其中 f* 为凯利准则给出的最优比例。

    :param win_probability: 获胜概率（0 < p < 1）
    :param win_loss_ratio: 赢得金额与损失金额之比（b > 0）
    :param fraction: 使用的凯利比例份额（0 < fraction <= 1），默认为 0.5
    :return: 分数凯利投注规模

    >>> round(fractional_kelly(0.6, 2.0, 0.5), 4)
    0.2
    >>> round(fractional_kelly(0.55, 1.0, 0.25), 4)
    0.025
    >>> round(fractional_kelly(0.7, 3.0, 1.0), 4)
    0.6
    >>> fractional_kelly(0.6, 2.0, 0.0)
    Traceback (most recent call last):
        ...
    ValueError: fraction must be between 0 and 1 (exclusive for 0, inclusive for 1)
    >>> fractional_kelly(0.6, 2.0, 1.5)
    Traceback (most recent call last):
        ...
    ValueError: fraction must be between 0 and 1 (exclusive for 0, inclusive for 1)
    >>> fractional_kelly(0.0, 2.0, 0.5)
    Traceback (most recent call last):
        ...
    ValueError: win_probability must be between 0 and 1 (exclusive)
    """
    if fraction <= 0 or fraction > 1:
        raise ValueError(
            "fraction must be between 0 and 1 (exclusive for 0, inclusive for 1)"
        )

    full_kelly = kelly_criterion(win_probability, win_loss_ratio)
    return fraction * full_kelly


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # 示例：获胜概率为 60%、赔率为 2:1 的投注
    win_prob = 0.6
    odds = 2.0
    full_kelly = kelly_criterion(win_prob, odds)
    half_kelly = fractional_kelly(win_prob, odds, 0.5)

    print(f"Win probability: {win_prob}")
    print(f"Win/loss ratio: {odds}")
    print(f"Full Kelly fraction: {full_kelly:.2%}")
    print(f"Half Kelly fraction: {half_kelly:.2%}")
