"""
Project Euler Problem 493: https://projecteuler.net/problem=493

一个瓮中放有 70 个彩球，七种彩虹颜色各有 10 个。
随机抽取 20 个球，球的不同颜色数量的期望是多少？
请将答案保留小数点后九位 (a.bcdefghij)。

-----

这个组合问题可以分解为以下步骤来求解：
1. 计算所有可能的抽取组合总数
[combinations := binom_coeff(70, 20)]
2. 计算缺少一种颜色的组合数
[missing := binom_coeff(60, 20)]
3. 计算缺少一种颜色的概率
[missing_prob := missing / combinations]
4. 计算不缺少任何颜色的概率
[no_missing_prob := 1 - missing_prob]
5. 计算不同颜色数量的期望
[expected = 7 * no_missing_prob]

参考资料：
- https://en.wikipedia.org/wiki/Binomial_coefficient
"""

import math

BALLS_PER_COLOUR = 10
NUM_COLOURS = 7
NUM_BALLS = BALLS_PER_COLOUR * NUM_COLOURS


def solution(num_picks: int = 20) -> str:
    """
    计算不同颜色数量的期望。

    >>> solution(10)
    '5.669644129'

    >>> solution(30)
    '6.985042712'
    """
    total = math.comb(NUM_BALLS, num_picks)
    missing_colour = math.comb(NUM_BALLS - BALLS_PER_COLOUR, num_picks)

    result = NUM_COLOURS * (1 - missing_colour / total)

    return f"{result:.9f}"


if __name__ == "__main__":
    print(solution(20))
