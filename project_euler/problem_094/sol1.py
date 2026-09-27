"""
Project Euler Problem 94: https://projecteuler.net/problem=94

很容易证明，不存在边长和面积均为整数的等边三角形。然而，近等边三角形 5-5-6
的面积为 12 平方单位。

将近等边三角形定义为两边相等、第三边与它们相差不超过一个单位的三角形。

求所有边长和面积均为整数、且周长不超过十亿 (1,000,000,000) 的近等边三角形周长之和。
"""


def solution(max_perimeter: int = 10**9) -> int:
    """
    返回所有边长和面积均为整数、且周长不超过 max_perimeter 的近等边三角形周长之和。

    >>> solution(20)
    16
    """

    prev_value = 1
    value = 2

    perimeters_sum = 0
    i = 0
    perimeter = 0
    while perimeter <= max_perimeter:
        perimeters_sum += perimeter

        prev_value += 2 * value
        value += prev_value

        perimeter = 2 * value + 2 if i % 2 == 0 else 2 * value - 2
        i += 1

    return perimeters_sum


if __name__ == "__main__":
    print(f"{solution() = }")
