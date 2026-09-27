"""
Problem 78
Url: https://projecteuler.net/problem=78
题目说明：
令 p(n) 表示将 n 枚硬币分成若干堆的不同方式数。例如，五枚硬币恰好可以用七种
不同方式分堆，因此 p(5)=7。

            OOOOO
            OOOO   O
            OOO   OO
            OOO   O   O
            OO   OO   O
            OO   O   O   O
            O   O   O   O   O
找出使 p(n) 能被一百万整除的最小 n 值。
"""

import itertools


def solution(number: int = 1000000) -> int:
    """
    >>> solution(1)
    1

    >>> solution(9)
    14

    >>> solution()
    55374
    """
    partitions = [1]

    for i in itertools.count(len(partitions)):
        item = 0
        for j in itertools.count(1):
            sign = -1 if j % 2 == 0 else +1
            index = (j * j * 3 - j) // 2
            if index > i:
                break
            item += partitions[i - index] * sign
            item %= number
            index += j
            if index > i:
                break
            item += partitions[i - index] * sign
            item %= number

        if item == 0:
            return i
        partitions.append(item)

    return 0


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print(f"{solution() = }")
