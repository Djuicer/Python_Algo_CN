"""
Project Euler Problem 85: https://projecteuler.net/problem=85

仔细计数可以看出，一个 3 x 2 的矩形网格包含十八个矩形。
￼
虽然不存在恰好包含两百万个矩形的矩形网格，但请找出最接近该数量的网格面积。

解法：

    对于边长为 a 和 b 的网格，其中包含的矩形数为
    [a*(a+1)/2] * [b*(b+1)/2)]，恰好是第 a 个与第 b 个三角数的乘积。
    因此要找解网格 (a,b)，需找出乘积最接近两百万的两个三角数。

    将这两个三角数记为 Ta 和 Tb，希望乘积 Ta*Tb 尽可能接近 2m。假设最佳解相当接近
    2m，则可认为 Ta 和 Tb 大致以 2m 为界。由于 Ta = a(a+1)/2，可认为 a（以及 b）
    大致以 sqrt(2 * 2m) = 2000 为界。这个界限较粗略，为安全起见增加 10%。
    因此先生成 1 <= a <= 2200 的所有三角数 Ta。由于第 i 个三角数是
    1,2, ... ,i 之和，即 T(i) = T(i-1) + i，可迭代完成。

    然后在三角数列表中搜索乘积最接近目标两百万的两个数。无需测试列表中每两个元素的
    所有组合（这会以平方时间求得结果），可以在线性时间内找到最佳数对。

    使用 enumerate() 遍历三角数列表，从而得到 a 和 Ta。由于希望 Ta * Tb 尽可能接近
    2m，Tb 应大致等于 2m / Ta。利用公式 Tb = b*(b+1)/2 和二次公式可解得 b：
    b 大致为 (-1 + sqrt(1 + 8 * 2m / Ta)) / 2。

    因为最接近该估计值的整数会给出最接近 2m 的乘积，所以只需考虑其上下两个整数。
    随后取得这些整数对应的三角数，计算乘积 Ta * Tb，与目标 2m 比较，
    并记录最接近目标的 (a,b) 数对。


Reference: https://en.wikipedia.org/wiki/Triangular_number
           https://en.wikipedia.org/wiki/Quadratic_formula
"""

from __future__ import annotations

from math import ceil, floor, sqrt


def solution(target: int = 2000000) -> int:
    """
    找出所含矩形数尽可能接近两百万的网格面积。
    >>> solution(20)
    6
    >>> solution(2000)
    72
    >>> solution(2000000000)
    86595
    """
    triangle_numbers: list[int] = [0]
    idx: int

    for idx in range(1, ceil(sqrt(target * 2) * 1.1)):
        triangle_numbers.append(triangle_numbers[-1] + idx)

    # 希望该值尽可能接近 target
    best_product: int = 0
    # 乘积最接近 target 的网格所对应的面积
    area: int = 0
    # 使用二次公式得到的 b 估计值
    b_estimate: float
    # 小于 b_estimate 的最大整数
    b_floor: int
    # 小于 b_estimate 的最大整数
    b_ceil: int
    # b_floor 对应的三角数
    triangle_b_first_guess: int
    # b_ceil 对应的三角数
    triangle_b_second_guess: int

    for idx_a, triangle_a in enumerate(triangle_numbers[1:], 1):
        b_estimate = (-1 + sqrt(1 + 8 * target / triangle_a)) / 2
        b_floor = floor(b_estimate)
        b_ceil = ceil(b_estimate)
        triangle_b_first_guess = triangle_numbers[b_floor]
        triangle_b_second_guess = triangle_numbers[b_ceil]

        if abs(target - triangle_b_first_guess * triangle_a) < abs(
            target - best_product
        ):
            best_product = triangle_b_first_guess * triangle_a
            area = idx_a * b_floor

        if abs(target - triangle_b_second_guess * triangle_a) < abs(
            target - best_product
        ):
            best_product = triangle_b_second_guess * triangle_a
            area = idx_a * b_ceil

    return area


if __name__ == "__main__":
    print(f"{solution() = }")
