"""
Project Euler Problem 138: https://projecteuler.net/problem=138

特殊等腰三角形


通过变量替换

c = b/2

并要求

h = 2c +- 1

三角形关系

c^2 + h^2 = L^2

可表示为

5 c^2 +- 4c + 1 = L^2

或者经过整理：

(5c +- 2)^2 = 5L^2 - 1

要使正整数 c 和 L 满足该式，需要

5L^2 - 1 = m^2

上述方程是 n = 5 时的负 Pell 方程，可按照 Wikipedia 文章所述递归求解。
注意，忽略第一个解 (m = 2, L = 1)，因为它会使 b 和 h 不是整数。

Reference: https://en.wikipedia.org/wiki/Pell%27s_equation#The_negative_Pell's_equation

"""


def solution(k: int = 12) -> int:
    """
    对负 Pell 方程进行递归求解，跳过第一个解，并对 k + 1 个 L 值求和。

    >>> solution(2)
    322
    >>> solution(5)
    1866293
    """

    m_i = 2
    l_i = 1
    ans = 0
    for _ in range(2, k + 2):
        m_i, l_i = 4 * m_i + 5 * m_i + 20 * l_i, 4 * l_i + 5 * l_i + 4 * m_i
        ans += l_i

    return ans


if __name__ == "__main__":
    print(f"{solution() = }")
