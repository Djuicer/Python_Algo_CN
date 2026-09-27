"""
此模块提供切割钢条问题的两类实现：
  1. 运行时间为指数级的朴素递归实现
  2. 两种运行时间为平方级的动态规划实现

切割钢条问题是在给定每种整数长度钢条的价格列表时，求长度为 ``n`` 的钢条
所能获得的最大收益。因此，可以将钢条切开并分别出售各段来获得最大收益；
如果整根钢条的价格就是可获得的最大值，也可以完全不切割。

"""


def naive_cut_rod_recursive(n: int, prices: list):
    """
    使用朴素方法求解切割钢条问题，不利用动态规划的优势。
    同一子问题会被多次求解，因此运行时间为指数级。

    运行时间：O(2^n)

    参数
    ---------

    * `n`: int，钢条长度。
    * `prices`: list，每段钢条的价格。``p[i-i]`` 是长度为 ``i`` 的钢条价格。

    返回
    -------

    给定各段价格列表时，长度为 `n` 的钢条可获得的最大收益。

    示例
    --------

    >>> naive_cut_rod_recursive(4, [1, 5, 8, 9])
    10
    >>> naive_cut_rod_recursive(10, [1, 5, 8, 9, 10, 17, 17, 20, 24, 30])
    30
    """

    _enforce_args(n, prices)
    if n == 0:
        return 0
    max_revue = float("-inf")
    for i in range(1, n + 1):
        max_revue = max(
            max_revue, prices[i - 1] + naive_cut_rod_recursive(n - i, prices)
        )

    return max_revue


def top_down_cut_rod(n: int, prices: list):
    """
    通过记忆化搜索构造切割钢条问题的自顶向下动态规划解法。
    此函数是 ``_top_down_cut_rod_recursive`` 的包装器。

    运行时间：O(n^2)

    参数
    ---------

    * `n`: int，钢条长度。
    * `prices`: list，每段钢条的价格。``p[i-i]`` 是长度为 ``i`` 的钢条价格。

    .. note::
      为方便起见，并且由于 Python 列表使用 ``0``-索引，令 ``length(max_rev)
      = n + 1``，以容纳长度为 ``0`` 的钢条可获得的收益。

    返回
    -------

    给定各段价格列表时，长度为 `n` 的钢条可获得的最大收益。

    示例
    --------

    >>> top_down_cut_rod(4, [1, 5, 8, 9])
    10
    >>> top_down_cut_rod(10, [1, 5, 8, 9, 10, 17, 17, 20, 24, 30])
    30
    """
    _enforce_args(n, prices)
    max_rev = [float("-inf") for _ in range(n + 1)]
    return _top_down_cut_rod_recursive(n, prices, max_rev)


def _top_down_cut_rod_recursive(n: int, prices: list, max_rev: list):
    """
    通过记忆化搜索构造切割钢条问题的自顶向下动态规划解法。

    运行时间：O(n^2)

    参数
    ---------

    * `n`: int，钢条长度。
    * `prices`: list，每段钢条的价格。``p[i-i]`` 是长度为 ``i`` 的钢条价格。
    * `max_rev`: list，已计算的钢条最大收益。
      ``max_rev[i]`` 是长度为 ``i`` 的钢条可获得的最大收益。

    返回
    -------

    给定各段价格列表时，长度为 `n` 的钢条可获得的最大收益。
    """
    if max_rev[n] >= 0:
        return max_rev[n]
    elif n == 0:
        return 0
    else:
        max_revenue = float("-inf")
        for i in range(1, n + 1):
            max_revenue = max(
                max_revenue,
                prices[i - 1] + _top_down_cut_rod_recursive(n - i, prices, max_rev),
            )

        max_rev[n] = max_revenue

    return max_rev[n]


def bottom_up_cut_rod(n: int, prices: list):
    """
    构造切割钢条问题的自底向上动态规划解法。

    运行时间：O(n^2)

    参数
    ---------

    * `n`: int，钢条的最大长度。
    * `prices`: list，每段钢条的价格。``p[i-i]`` 是长度为 ``i`` 的钢条价格。

    返回
    -------

    给定每段钢条 p 的价格时，切割长度为 `n` 的钢条可获得的最大收益。

    示例
    --------

    >>> bottom_up_cut_rod(4, [1, 5, 8, 9])
    10
    >>> bottom_up_cut_rod(10, [1, 5, 8, 9, 10, 17, 17, 20, 24, 30])
    30
    """
    _enforce_args(n, prices)

    # length(max_rev) = n + 1，以容纳长度为 0 的钢条可获得的收益
    max_rev = [float("-inf") for _ in range(n + 1)]
    max_rev[0] = 0

    for i in range(1, n + 1):
        max_revenue_i = max_rev[i]
        for j in range(1, i + 1):
            max_revenue_i = max(max_revenue_i, prices[j - 1] + max_rev[i - j])

        max_rev[i] = max_revenue_i

    return max_rev[n]


def _enforce_args(n: int, prices: list) -> None:
    """
    对切割钢条算法的参数执行基本检查。

    * `n`: int，钢条长度。
    * `prices`: list，每段钢条的价格列表。

    抛出 ``ValueError``：
        如果 `n` 为负数，或者价格列表中的项目数少于钢条长度。
    """
    if n < 0:
        msg = f"n must be greater than or equal to 0. Got n = {n}"
        raise ValueError(msg)

    if n > len(prices):
        msg = (
            "Each integral piece of rod must have a corresponding price. "
            f"Got n = {n} but length of prices = {len(prices)}"
        )
        raise ValueError(msg)


def main() -> None:
    prices = [6, 10, 12, 15, 20, 23]
    n = len(prices)

    # 最佳收益来自将钢条切成 6 段，每段长度为 1，收益为 6 * 6 = 36
    expected_max_revenue = 36

    max_rev_top_down = top_down_cut_rod(n, prices)
    max_rev_bottom_up = bottom_up_cut_rod(n, prices)
    max_rev_naive = naive_cut_rod_recursive(n, prices)

    assert expected_max_revenue == max_rev_top_down
    assert max_rev_top_down == max_rev_bottom_up
    assert max_rev_bottom_up == max_rev_naive


if __name__ == "__main__":
    main()
