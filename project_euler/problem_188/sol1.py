"""
Project Euler Problem 188: https://projecteuler.net/problem=188

数的超幂

数 a 关于正整数 b 的超幂（或幂塔）记作 a↑↑b 或 b^a，递归定义为：

a↑↑1 = a,
a↑↑(k+1) = a(a↑↑k).

因此，例如 3↑↑2 = 3^3 = 27，进而 3↑↑3 = 3^27 = 7625597484987，且
3↑↑4 约为 103.6383346400240996*10^12。

求 1777↑↑1855 的末 8 位数字。

References:
    - https://en.wikipedia.org/wiki/Tetration
"""


# 模幂运算的小型辅助函数（快速幂算法）
def _modexpt(base: int, exponent: int, modulo_value: int) -> int:
    """
    返回模幂运算结果，即 `base ** exponent % modulo_value` 的值，
    而不计算实际数值。
    >>> _modexpt(2, 4, 10)
    6
    >>> _modexpt(2, 1024, 100)
    16
    >>> _modexpt(13, 65535, 7)
    6
    """

    if exponent == 1:
        return base
    if exponent % 2 == 0:
        x = _modexpt(base, exponent // 2, modulo_value) % modulo_value
        return (x * x) % modulo_value
    else:
        return (base * _modexpt(base, exponent - 1, modulo_value)) % modulo_value


def solution(base: int = 1777, height: int = 1855, digits: int = 8) -> int:
    """
    返回 base 关于 height 的超幂（即 base↑↑height）的末 8 位数字：

    >>> solution(base=3, height=2)
    27
    >>> solution(base=3, height=3)
    97484987
    >>> solution(base=123, height=456, digits=4)
    2547
    """

    # 通过右结合的重复模幂运算计算 base↑↑height
    result = base
    for _ in range(1, height):
        result = _modexpt(base, result, 10**digits)

    return result


if __name__ == "__main__":
    print(f"{solution() = }")
