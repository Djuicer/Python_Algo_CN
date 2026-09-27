"""
Problem 120 Square remainders: https://projecteuler.net/problem=120

说明：

令 r 为 (a-1)^n + (a+1)^n 除以 a^2 的余数。
例如，当 a = 7 且 n = 3 时，r = 42：6^3 + 8^3 = 728 ≡ 42 mod 49。
随着 n 变化，r 也会变化；但当 a = 7 时，r_max = 42。对于 3 ≤ a ≤ 1000，求 ∑ r_max。

解法：

展开各项后，n 为偶数时得到 2，n 为奇数时得到 2an。
为使该值最大，2an < a*a => n <= (a - 1)/2（整数除法）
"""


def solution(n: int = 1000) -> int:
    """
    返回上述 3 <= a <= n 时的 ∑ r_max。
    >>> solution(10)
    300
    >>> solution(100)
    330750
    >>> solution(1000)
    333082500
    """
    return sum(2 * a * ((a - 1) // 2) for a in range(3, n + 1))


if __name__ == "__main__":
    print(solution())
