"""
现有 m 种数量无限的硬币，每种硬币的面值由数组 S=[S0,... Sm-1] 给出。
能否确定使用这些硬币凑成 n 单位金额的方式数？
https://www.hackerrank.com/challenges/coin-change/problem
"""


def dp_count(s, n):
    """
    >>> dp_count([1, 2, 3], 4)
    4
    >>> dp_count([1, 2, 3], 7)
    8
    >>> dp_count([2, 5, 3, 6], 10)
    5
    >>> dp_count([10], 99)
    0
    >>> dp_count([4, 5, 6], 0)
    1
    >>> dp_count([1, 2, 3], -5)
    0
    """
    if n < 0:
        return 0
    # table[i] 表示凑成金额 i 的方式数
    table = [0] * (n + 1)

    # 凑成零恰好有 1 种方式（不选择任何硬币）
    table[0] = 1

    # 逐一选择所有硬币，并更新索引大于或等于所选硬币面值的 table[] 值
    for coin_val in s:
        for j in range(coin_val, n + 1):
            table[j] += table[j - coin_val]

    return table[n]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
