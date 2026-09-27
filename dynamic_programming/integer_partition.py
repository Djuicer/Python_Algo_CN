"""
将数 n 划分为至少 k 部分的划分数，等于恰好划分为 k 部分的划分数，
加上至少划分为 k-1 部分的划分数。
从 n 的一个 k 部分划分中的每个部分减去 1，会得到 n-k 的一个 k 部分划分。
本算法综合使用这两个事实。
* https://en.wikipedia.org/wiki/Partition_(number_theory)
* https://en.wikipedia.org/wiki/Partition_function_(number_theory)
"""


def partition(m: int) -> int:
    """
    >>> partition(5)
    7
    >>> partition(7)
    15
    >>> partition(100)
    190569292
    >>> partition(1_000)
    24061467864032622473692149727991
    >>> partition(-7)
    Traceback (most recent call last):
        ...
    IndexError: list index out of range
    >>> partition(0)
    Traceback (most recent call last):
        ...
    IndexError: list assignment index out of range
    >>> partition(7.8)
    Traceback (most recent call last):
        ...
    TypeError: 'float' object cannot be interpreted as an integer
    """
    memo: list[list[int]] = [[0 for _ in range(m)] for _ in range(m + 1)]
    for i in range(m + 1):
        memo[i][0] = 1

    for n in range(m + 1):
        for k in range(1, m):
            memo[n][k] += memo[n][k - 1]
            if n - k > 0:
                memo[n][k] += memo[n - k - 1][k]

    return memo[m][m - 1]


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        try:
            n = int(input("Enter a number: ").strip())
            print(partition(n))
        except ValueError:
            print("Please enter a number.")
    else:
        try:
            n = int(sys.argv[1])
            print(partition(n))
        except ValueError:
            print("Please pass a number.")
