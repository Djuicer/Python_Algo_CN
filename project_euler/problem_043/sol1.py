"""
Problem 43: https://projecteuler.net/problem=43

数字 1406357289 是一个 0 到 9 的全数字数，因为它以某种顺序包含了 0 到 9
的每个数字；它还具有一种有趣的子串整除性质。

令 d1 为第 1 位、d2 为第 2 位，依此类推。于是有：

d2d3d4=406 可被 2 整除
d3d4d5=063 可被 3 整除
d4d5d6=635 可被 5 整除
d5d6d7=357 可被 7 整除
d6d7d8=572 可被 11 整除
d7d8d9=728 可被 13 整除
d8d9d10=289 可被 17 整除
求所有具有此性质的 0 到 9 全数字数之和。
"""

from itertools import permutations


def is_substring_divisible(num: tuple) -> bool:
    """
    如果全数字数通过所有整除测试，则返回 True。
    >>> is_substring_divisible((0, 1, 2, 4, 6, 5, 7, 3, 8, 9))
    False
    >>> is_substring_divisible((5, 1, 2, 4, 6, 0, 7, 8, 3, 9))
    False
    >>> is_substring_divisible((1, 4, 0, 6, 3, 5, 7, 2, 8, 9))
    True
    """
    if num[3] % 2 != 0:
        return False

    if (num[2] + num[3] + num[4]) % 3 != 0:
        return False

    if num[5] % 5 != 0:
        return False

    tests = [7, 11, 13, 17]
    for i, test in enumerate(tests):
        if (num[i + 4] * 100 + num[i + 5] * 10 + num[i + 6]) % test != 0:
            return False
    return True


def solution(n: int = 10) -> int:
    """
    返回通过整除测试的所有全数字数之和。
    >>> solution(10)
    16695334890
    """
    return sum(
        int("".join(map(str, num)))
        for num in permutations(range(n))
        if is_substring_divisible(num)
    )


if __name__ == "__main__":
    print(f"{solution() = }")
