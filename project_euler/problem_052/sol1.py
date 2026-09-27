"""
排列倍数
Problem 52

可以看出，数字 125874 及其两倍 251748 所含数字完全相同，只是顺序不同。

找出最小正整数 x，使 2x, 3x, 4x, 5x 和 6x 包含相同的数字。
"""


def solution():
    """返回使 2x, 3x, 4x, 5x 和 6x 包含相同数字的最小正整数 x。

    >>> solution()
    142857
    """
    i = 1

    while True:
        if (
            sorted(str(i))
            == sorted(str(2 * i))
            == sorted(str(3 * i))
            == sorted(str(4 * i))
            == sorted(str(5 * i))
            == sorted(str(6 * i))
        ):
            return i

        i += 1


if __name__ == "__main__":
    print(solution())
