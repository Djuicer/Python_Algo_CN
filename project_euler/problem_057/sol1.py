"""
Project Euler Problem 57: https://projecteuler.net/problem=57
可以证明，2 的平方根可表示为无限连分数。

sqrt(2) = 1 + 1 / (2 + 1 / (2 + 1 / (2 + ...)))

将其展开前四次，得到：
1 + 1 / 2 = 3 / 2 = 1.5
1 + 1 / (2 + 1 / 2} = 7 / 5 = 1.4
1 + 1 / (2 + 1 / (2 + 1 / 2)) = 17 / 12 = 1.41666...
1 + 1 / (2 + 1 / (2 + 1 / (2 + 1 / 2))) = 41/ 29 = 1.41379...

接下来的三个展开式为 99/70, 239/169 和 577/408；而第八个展开式 1393/985
首次出现分子位数多于分母位数的情况。

在前一千个展开式中，有多少个分数的分子位数多于分母位数？
"""


def solution(n: int = 1000) -> int:
    """
    返回前 n 个展开式中分子位数多于分母位数的分数数量。
    >>> solution(14)
    2
    >>> solution(100)
    15
    >>> solution(10000)
    1508
    """
    prev_numerator, prev_denominator = 1, 1
    result = []
    for i in range(1, n + 1):
        numerator = prev_numerator + 2 * prev_denominator
        denominator = prev_numerator + prev_denominator
        if len(str(numerator)) > len(str(denominator)):
            result.append(i)
        prev_numerator = numerator
        prev_denominator = denominator

    return len(result)


if __name__ == "__main__":
    print(f"{solution() = }")
