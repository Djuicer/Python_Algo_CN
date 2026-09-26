from __future__ import annotations

from maths.greatest_common_divisor import greatest_common_divisor


def diophantine(a: int, b: int, c: int) -> tuple[float, float]:
    """
    丢番图方程（Diophantine Equation）：给定整数 a、b、c（a 和 b 至少一个不为
    0），当且仅当 greatest_common_divisor(a,b) 能整除 c 时，丢番图方程
    a*x + b*y = c 才有整数解 x 和 y。

    GCD（最大公约数，Greatest Common Divisor）或 HCF（最高公因数，
    Highest Common Factor）

    >>> diophantine(10,6,14)
    (-7.0, 14.0)

    >>> diophantine(391,299,-69)
    (9.0, -12.0)

    但上述方程还有另一个解，即 x = -4、y = 5。
    因此需要使用求丢番图方程全部解的函数。

    """

    assert (
        c % greatest_common_divisor(a, b) == 0
    )  # greatest_common_divisor(a,b) 位于 maths 目录中
    (d, x, y) = extended_gcd(a, b)  # extended_gcd(a,b) 函数在下方实现
    r = c / d
    return (r * x, r * y)


def diophantine_all_soln(a: int, b: int, c: int, n: int = 2) -> None:
    """
    引理：如果 n|ab 且 gcd(a,n) = 1，则 n|b。

    求丢番图方程的所有解：

    定理：令 gcd(a,b) = d、a = d*p、b = d*q。如果 (x0,y0) 是丢番图方程
    a*x + b*y = c 的一个解，即 a*x0 + b*y0 = c，则所有解均可写成
    a(x0 + t*q) + b(y0 - t*p) = c，其中 t 为任意整数。

    n 是所需解的数量，默认值为 2。

    >>> diophantine_all_soln(10, 6, 14)
    -7.0 14.0
    -4.0 9.0

    >>> diophantine_all_soln(10, 6, 14, 4)
    -7.0 14.0
    -4.0 9.0
    -1.0 4.0
    2.0 -1.0

    >>> diophantine_all_soln(391, 299, -69, n = 4)
    9.0 -12.0
    22.0 -29.0
    35.0 -46.0
    48.0 -63.0

    """
    (x0, y0) = diophantine(a, b, c)  # 初始值
    d = greatest_common_divisor(a, b)
    p = a // d
    q = b // d

    for i in range(n):
        x = x0 + i * q
        y = y0 - i * p
        print(x, y)


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    扩展欧几里得算法（Extended Euclidean Algorithm）：如果 d 能整除 a 和 b，
    且对于整数 x 和 y 有 d = a*x + b*y，则 d = gcd(a,b)。

    >>> extended_gcd(10, 6)
    (2, -1, 2)

    >>> extended_gcd(7, 5)
    (1, -2, 3)

    """
    assert a >= 0
    assert b >= 0

    if b == 0:
        d, x, y = a, 1, 0
    else:
        (d, p, q) = extended_gcd(b, a % b)
        x = q
        y = p - q * (a // b)

    assert a % d == 0
    assert b % d == 0
    assert d == a * x + b * y

    return (d, x, y)


def all_diophantine_solutions(
    a: int,
    b: int,
    c: int,
    n: int = 2,
) -> list[tuple[int, int]]:
    """
    使用扩展欧几里得算法，返回线性丢番图方程 a*x + b*y = c 的至多 `n` 个
    整数解 (x, y)。

    异常
    ------
    ValueError
        不存在整数解时引发。

    时间复杂度
    ---------------
    使用 extended_gcd 计算一个基础解需要 O(log(max(|a|, |b|)))；
    枚举 `n` 个解还需要 O(n)。

    空间复杂度
    ----------------
    除返回列表外为 O(1)。

    示例
    --------
    >>> all_diophantine_solutions(10, 6, 14, n=2)
    [(-7, 14), (-4, 9)]
    >>> all_diophantine_solutions(10, 6, 14, n=4)
    [(-7, 14), (-4, 9), (-1, 4), (2, -1)]
    >>> all_diophantine_solutions(3, 6, 10, n=1)
    Traceback (most recent call last):
    ...
    ValueError: No integer solutions exist for a=3, b=6, c=10
    """
    if a == 0 and b == 0:
        if c == 0:
            # 有无穷多个解；返回一个规范解。
            return [(0, 0)][: min(1, n)]
        raise ValueError("No integer solutions exist for a=0, b=0, c!=0")

    g, xg, yg = extended_gcd(abs(a), abs(b))
    if c % g != 0:
        msg = f"No integer solutions exist for a={a}, b={b}, c={c}"
        raise ValueError(msg)

    # 将一个特解缩放为 ax + by = c 的解
    x0, y0 = xg * (c // g), yg * (c // g)
    if a < 0:
        x0 = -x0
    if b < 0:
        y0 = -y0

    # 通解：x = x0 + t*(b/g)，y = y0 - t*(a/g)
    dx, dy = b // g, a // g
    return [(x0 + t * dx, y0 - t * dy) for t in range(n)]


if __name__ == "__main__":
    from doctest import testmod

    testmod(name="diophantine", verbose=True)
    testmod(name="diophantine_all_soln", verbose=True)
    testmod(name="extended_gcd", verbose=True)
    testmod(name="greatest_common_divisor", verbose=True)
