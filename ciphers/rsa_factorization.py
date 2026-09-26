"""
RSA 素因数分解算法。

给定私钥 d 和公钥 e，本程序可高效分解 RSA 素数。

| 来源：https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf 第 ``3`` 页
| 更易读的资料：https://www.di-mgt.com.au/rsa_factorize_n.html

大数分解可能耗时数分钟，因此未纳入 doctest。
"""

from __future__ import annotations

import math
import random


def rsafactor(d: int, e: int, n: int) -> list[int]:
    """
    返回 N 的因数，其中 p*q=N。

    返回值：[p, q]

    N 称为 RSA 模数，e 为加密指数，d 为解密指数。二元组 (N, e) 是公钥；顾名思义，
    它是公开的，用于加密消息。二元组 (N, d) 是秘密密钥或私钥，仅加密消息的
    接收者知晓。

    >>> rsafactor(3, 16971, 25777)
    [149, 173]
    >>> rsafactor(7331, 11, 27233)
    [113, 241]
    >>> rsafactor(4021, 13, 17711)
    [89, 199]
    """
    k = d * e - 1
    p = 0
    q = 0
    while p == 0:
        g = random.randint(2, n - 1)
        t = k
        while True:
            if t % 2 == 0:
                t = t // 2
                x = (g**t) % n
                y = math.gcd(x - 1, n)
                if x > 1 and y > 1:
                    p = y
                    q = n // y
                    break  # 找到正确因数
            else:
                break  # t 不能被 2 整除，退出并选择另一个 g
    return sorted([p, q])


if __name__ == "__main__":
    import doctest

    doctest.testmod()
