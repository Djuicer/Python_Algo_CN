"""
Project Euler Problem 203: https://projecteuler.net/problem=203

二项式系数 (n k) 可以排列成如下三角形形式，即 Pascal 三角形：
                            1
                        1       1
                    1		2       1
                1		3		3       1
            1		4		6		4		1
        1		5		10		10		5		1
    1		6		15		20		15		6		1
1		7		21		35		35		21		7		1
                        .........

可以看出，Pascal 三角形的前八行包含十二个不同数字：
1, 2, 3, 4, 5, 6, 7, 10, 15, 20, 21 and 35。

若正整数 n 不可被任何素数的平方整除，则称 n 为无平方因子数。
Pascal 三角形前八行的十二个不同数字中，除 4 和 20 外均为无平方因子数。
前八行中不同无平方因子数的总和为 105。

求 Pascal 三角形前 51 行中不同无平方因子数的总和。

References:
- https://en.wikipedia.org/wiki/Pascal%27s_triangle
"""

from __future__ import annotations


def get_pascal_triangle_unique_coefficients(depth: int) -> set[int]:
    """
    返回深度为 "depth" 的 Pascal 三角形中的不同系数。

    该三角形的系数具有对称性。可以通过每层只计算一次系数进一步改进此方法，
    但当前实现对原题而言已足够快。

    >>> get_pascal_triangle_unique_coefficients(1)
    {1}
    >>> get_pascal_triangle_unique_coefficients(2)
    {1}
    >>> get_pascal_triangle_unique_coefficients(3)
    {1, 2}
    >>> get_pascal_triangle_unique_coefficients(8)
    {1, 2, 3, 4, 5, 6, 7, 35, 10, 15, 20, 21}
    """
    coefficients = {1}
    previous_coefficients = [1]
    for _ in range(2, depth + 1):
        coefficients_begins_one = [*previous_coefficients, 0]
        coefficients_ends_one = [0, *previous_coefficients]
        previous_coefficients = []
        for x, y in zip(coefficients_begins_one, coefficients_ends_one):
            coefficients.add(x + y)
            previous_coefficients.append(x + y)
    return coefficients


def get_squarefrees(unique_coefficients: set[int]) -> set[int]:
    """
    计算 unique_coefficients 中的无平方因子数。

    根据非无平方因子数的定义，任何此类 n 都可分解为 n = p*p*r，
    其中 p 是正素数，r 是正整数。

    根据上述公式，由于 r 不能为负，任何小于 p*p 的系数都是无平方因子数。
    反之，若存在 r 使 n = p*p*r，则该数不是无平方因子数。

    >>> get_squarefrees({1})
    {1}
    >>> get_squarefrees({1, 2})
    {1, 2}
    >>> get_squarefrees({1, 2, 3, 4, 5, 6, 7, 35, 10, 15, 20, 21})
    {1, 2, 3, 5, 6, 7, 35, 10, 15, 21}
    """

    non_squarefrees = set()
    for number in unique_coefficients:
        divisor = 2
        copy_number = number
        while divisor**2 <= copy_number:
            multiplicity = 0
            while copy_number % divisor == 0:
                copy_number //= divisor
                multiplicity += 1
            if multiplicity >= 2:
                non_squarefrees.add(number)
                break
            divisor += 1

    return unique_coefficients.difference(non_squarefrees)


def solution(n: int = 51) -> int:
    """
    返回给定深度 n 的 Pascal 三角形中无平方因子数的总和。

    >>> solution(1)
    1
    >>> solution(8)
    105
    >>> solution(9)
    175
    """
    unique_coefficients = get_pascal_triangle_unique_coefficients(n)
    squarefrees = get_squarefrees(unique_coefficients)
    return sum(squarefrees)


if __name__ == "__main__":
    print(f"{solution() = }")
