"""
组合选择
Problem 53

从五个元素 12345 中选择三个，恰好有十种方式：

    123, 124, 125, 134, 135, 145, 234, 235, 245, 和 345

在组合数学中，记作 5C3 = 10。

一般而言，

nCr = n!/(r!(n-r)!)，其中 r ≤ n，n! = nx(n-1)x...x3x2x1，且 0! = 1。
直到 n = 23，才有一个值超过一百万：23C10 = 1144066。

对于 1 ≤ n ≤ 100，有多少个（不要求互不相同的）nCr 值大于一百万？
"""

from math import factorial


def combinations(n, r):
    return factorial(n) / (factorial(r) * factorial(n - r))


def solution():
    """返回 1 ≤ n ≤ 100 时大于一百万的 nCr 值的数量。

    >>> solution()
    4075
    """
    total = 0

    for i in range(1, 101):
        for j in range(1, i + 1):
            if combinations(i, j) > 1e6:
                total += 1
    return total


if __name__ == "__main__":
    print(solution())
