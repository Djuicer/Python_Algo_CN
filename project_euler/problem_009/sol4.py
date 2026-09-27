"""
Project Euler Problem 9: https://projecteuler.net/problem=9

特殊勾股数

勾股数是满足 a < b < c 的三个自然数 a、b、c，且：

    a^2 + b^2 = c^2.

例如，3^2 + 4^2 = 9 + 16 = 25 = 5^2。

恰有一组勾股数满足 a + b + c = 1000。求乘积 abc。

参考资料：
    - https://en.wikipedia.org/wiki/Pythagorean_triple
"""


def get_squares(n: int) -> list[int]:
    """
    >>> get_squares(0)
    []
    >>> get_squares(1)
    [0]
    >>> get_squares(2)
    [0, 1]
    >>> get_squares(3)
    [0, 1, 4]
    >>> get_squares(4)
    [0, 1, 4, 9]
    """
    return [number * number for number in range(n)]


def solution(n: int = 1000) -> int:
    """
    预先计算平方数，并通过集合查找检查 a^2 + b^2 是否为平方数。

    >>> solution(12)
    60
    >>> solution(36)
    1620
    """

    squares = get_squares(n)
    squares_set = set(squares)
    for a in range(1, n // 3):
        for b in range(a + 1, (n - a) // 2 + 1):
            if (
                squares[a] + squares[b] in squares_set
                and squares[n - a - b] == squares[a] + squares[b]
            ):
                return a * b * (n - a - b)

    return -1


if __name__ == "__main__":
    print(f"{solution() = }")
