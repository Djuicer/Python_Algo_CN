"""
Problem 123: https://projecteuler.net/problem=123

名称：素数平方余数

令 pn 为第 n 个素数：2, 3, 5, 7, 11, ...；令 r 为
(pn-1)^n + (pn+1)^n 除以 pn^2 的余数。

例如，当 n = 3 时，p3 = 5，且 43 + 63 = 280 ≡ 5 mod 25。
余数首次超过 10^9 时的最小 n 值为 7037。

求余数首次超过 10^10 时的最小 n 值。


解法：

n=1: (p-1) + (p+1) = 2p
n=2: (p-1)^2 + (p+1)^2
     = p^2 + 1 - 2p + p^2 + 1 + 2p  (使用 (p+b)^2 = (p^2 + b^2 + 2pb),
                                           (p-b)^2 = (p^2 + b^2 - 2pb)，且 b = 1)
     = 2p^2 + 2
n=3: (p-1)^3 + (p+1)^3  (类似地使用 (p+b)^3 & (p-b)^3 公式，依此类推)
     = 2p^3 + 6p
n=4: 2p^4 + 12p^2 + 2
n=5: 2p^5 + 20p^3 + 10p

可以看出，当表达式除以 p^2 时，除最后一项外，其余各项的余数均为 0。

n=1: 2p
n=2: 2
n=3: 6p
n=4: 2
n=5: 10p

因此可简化为：
    n 为奇数时，r = 2pn
    n 为偶数时，r = 2。
"""

from __future__ import annotations

from collections.abc import Generator


def sieve() -> Generator[int]:
    """
    返回使用筛法的素数生成器。
    >>> type(sieve())
    <class 'generator'>
    >>> primes = sieve()
    >>> next(primes)
    2
    >>> next(primes)
    3
    >>> next(primes)
    5
    >>> next(primes)
    7
    >>> next(primes)
    11
    >>> next(primes)
    13
    """
    factor_map: dict[int, int] = {}
    prime = 2
    while True:
        factor = factor_map.pop(prime, None)
        if factor:
            x = factor + prime
            while x in factor_map:
                x += factor
            factor_map[x] = factor
        else:
            factor_map[prime * prime] = prime
            yield prime
        prime += 1


def solution(limit: float = 1e10) -> int:
    """
    返回余数首次超过 10^10 时的最小 n 值。
    >>> solution(1e8)
    2371
    >>> solution(1e9)
    7037
    """
    primes = sieve()

    n = 1
    while True:
        prime = next(primes)
        if (2 * prime * n) > limit:
            return n
        # 忽略下一个素数，因为余数将为 2
        next(primes)
        n += 2


if __name__ == "__main__":
    print(solution())
