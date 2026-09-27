"""
Project Euler Problem 136: https://projecteuler.net/problem=136

唯一解差值

正整数 x、y 和 z 是等差数列的连续项。给定正整数 n，当 n = 20 时，方程
x^2 - y^2 - z^2 = n 恰有一个解：
                              13^2 - 10^2 - 7^2 = 20.

事实上，一百以下共有二十五个 n 值使该方程具有唯一解。

小于五千万且恰有一个解的 n 有多少个？

通过变量替换

x = y + delta
z = y - delta

表达式可改写为：

x^2 - y^2 - z^2 = y * (4 * delta - y) = n

算法遍历 delta 和 y（y 受上下界约束），统计每个 n 的解数。
最后统计恰有一个解的 n 的数量。
"""


def solution(n_limit: int = 50 * 10**6) -> int:
    """
    定义 n 的计数列表并遍历 delta、y 以获得计数，然后检查哪些 n 的计数为 1。

    >>> solution(3)
    0
    >>> solution(10)
    3
    >>> solution(100)
    25
    >>> solution(110)
    27
    """
    n_sol = [0] * n_limit

    for delta in range(1, (n_limit + 1) // 4 + 1):
        for y in range(4 * delta - 1, delta, -1):
            n = y * (4 * delta - y)
            if n >= n_limit:
                break
            n_sol[n] += 1

    ans = 0
    for i in range(n_limit):
        if n_sol[i] == 1:
            ans += 1

    return ans


if __name__ == "__main__":
    print(f"{solution() = }")
