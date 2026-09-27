"""
完全数是其真约数之和恰好等于自身的数。例如，28 的真约数之和为
1 + 2 + 4 + 7 + 14 = 28，因此 28 是完全数。

如果数 n 的真约数之和小于 n，则称 n 为亏数；如果该和大于 n，则称 n 为盈数。

由于 12 是最小的盈数，1 + 2 + 3 + 4 + 6 = 16，所以能写成两个盈数之和的
最小数是 24。通过数学分析可以证明，所有大于 28123 的整数都能写成两个盈数之和。
然而，即使已知不能表示为两个盈数之和的最大数小于此界限，也无法仅通过分析进一步
降低这个上界。

求所有不能写成两个盈数之和的正整数之和。
"""


def solution(limit=28123):
    """
    求出上述题意中所有不能写成两个盈数之和的正整数之和。

    >>> solution()
    4179871
    """
    sum_divs = [1] * (limit + 1)

    for i in range(2, int(limit**0.5) + 1):
        sum_divs[i * i] += i
        for k in range(i + 1, limit // i + 1):
            sum_divs[k * i] += k + i

    abundants = set()
    res = 0

    for n in range(1, limit + 1):
        if sum_divs[n] > n:
            abundants.add(n)

        if not any((n - a in abundants) for a in abundants):
            res += n

    return res


if __name__ == "__main__":
    print(solution())
