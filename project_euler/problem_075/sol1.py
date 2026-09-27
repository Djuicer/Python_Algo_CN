"""
Project Euler Problem 75: https://projecteuler.net/problem=75

事实证明，12 cm 是能够以恰好一种方式弯成整数边直角三角形的最短金属丝长度，
但还有许多其他示例。

12 cm: (3,4,5)
24 cm: (6,8,10)
30 cm: (5,12,13)
36 cm: (9,12,15)
40 cm: (8,15,17)
48 cm: (12,16,20)

相比之下，某些长度的金属丝（如 20 cm）无法弯成整数边直角三角形；另一些长度则有
多个解。例如，使用 120 cm 金属丝恰好可以形成三个不同的整数边直角三角形。

120 cm: (30,40,50), (20,48,52), (24,45,51)

设 L 为金属丝长度，在 L ≤ 1,500,000 的取值中，有多少个恰好能形成一个整数边
直角三角形？

解法：使用 Euclid 公式生成所有勾股数，并记录各周长出现的次数。

参考资料：https://en.wikipedia.org/wiki/Pythagorean_triple#Generating_a_triple
"""

from collections import defaultdict
from math import gcd


def solution(limit: int = 1500000) -> int:
    """
    返回满足 L <= limit 且长度为 L 的金属丝恰好能以一种方式形成整数边直角三角形的
    L 值数量。
    >>> solution(50)
    6
    >>> solution(1000)
    112
    >>> solution(50000)
    5502
    """
    frequencies: defaultdict = defaultdict(int)
    euclid_m = 2
    while 2 * euclid_m * (euclid_m + 1) <= limit:
        for euclid_n in range((euclid_m % 2) + 1, euclid_m, 2):
            if gcd(euclid_m, euclid_n) > 1:
                continue
            primitive_perimeter = 2 * euclid_m * (euclid_m + euclid_n)
            for perimeter in range(primitive_perimeter, limit + 1, primitive_perimeter):
                frequencies[perimeter] += 1
        euclid_m += 1
    return sum(1 for frequency in frequencies.values() if frequency == 1)


if __name__ == "__main__":
    print(f"{solution() = }")
