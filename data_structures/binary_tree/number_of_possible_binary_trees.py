"""
Hey，我们 是 going 到 查找 exciting 数 called Catalan 数 其 是 使用 到 查找
数 的 可能 binary 搜索 树 从 树 的 给定 节点数量。

我们 将 使用 formula: t(n) = SUMMATION(i = 1 到 n)t(i-1)t(n-i)

Further details at Wikipedia: https://en.wikipedia.org/wiki/Catalan_number
"""

"""
Our Contribution:
Basically we Create the 2 function:
    1. catalan_number(node_count: int) -> int
        Returns the number of possible binary search trees for n nodes.
    2. binary_tree_count(node_count: int) -> int
        Returns the number of possible binary trees for n nodes.
"""


def binomial_coefficient(n: int, k: int) -> int:
    """
    Since 此处 我们 查找 Binomial Coefficient：
    https://en.wikipedia.org/wiki/Binomial_coefficient
    C(n,k) = n! / k!(n-k)!
    :param n: 2 times 的 节点数量
    :param k: 节点数量
    :返回:  整数 值

    >>> binomial_coefficient(4, 2)
    6
    """
    result = 1  # 到 kept 计算得出 值
    # Since C(n, k) = C(n, n-k)
    k = min(k, n - k)
    # 计算 C(n,k)
    for i in range(k):
        result *= n - i
        result //= i + 1
    return result


def catalan_number(node_count: int) -> int:
    """
    我们 可以 查找 Catalan 数 many ways 但是 此处 我们 使用 Binomial Coefficient 因为 它
    does job 在 O(n)

    返回 Catalan 数 的 n 使用 2nCn/(n+1)。
    :param n: 节点数量
    :返回: Catalan 数 的 n 节点

    >>> catalan_number(5)
    42
    >>> catalan_number(6)
    132
    """
    return binomial_coefficient(2 * node_count, node_count) // (node_count + 1)


def factorial(n: int) -> int:
    """
    返回 factorial 的 数。
    :param n: 数 到 查找 Factorial 的。
    :返回: Factorial 的 n。

    >>> import math
    >>> all(factorial(i) == math.factorial(i) for i in range(10))
    True
    >>> factorial(-5)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: factorial() not defined for negative values
    """
    if n < 0:
        raise ValueError("factorial() not defined for negative values")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def binary_tree_count(node_count: int) -> int:
    """
    返回以下对象的数量： 可能 的 binary 树。
    :param n: 节点数量
    :返回: 数 的 可能 binary 树

    >>> binary_tree_count(5)
    5040
    >>> binary_tree_count(6)
    95040
    """
    return catalan_number(node_count) * factorial(node_count)


if __name__ == "__main__":
    node_count = int(input("Enter the number of nodes: ").strip() or 0)
    if node_count <= 0:
        raise ValueError("We need some nodes to work with.")
    print(
        f"Given {node_count} nodes, there are {binary_tree_count(node_count)} "
        f"binary trees and {catalan_number(node_count)} binary search trees."
    )
