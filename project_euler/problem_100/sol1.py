"""
Project Euler Problem 100: https://projecteuler.net/problem=100

若一个盒子包含二十一个彩色圆片，其中十五个蓝色、六个红色，并随机取出两个圆片，
则可看出取到两个蓝色圆片的概率 P(BB) = (15/21) x (14/20) = 1/2。

下一个随机取到两个蓝色圆片的概率恰为 50% 的配置，是盒中有八十五个蓝色圆片和
三十五个红色圆片。

找出总圆片数首次超过 10^12 = 1,000,000,000,000 的配置，并确定盒中蓝色圆片的数量。
"""


def solution(min_total: int = 10**12) -> int:
    """
    返回总圆片数首次超过 min_total 的配置中蓝色圆片的数量。

    >>> solution(2)
    3

    >>> solution(4)
    15

    >>> solution(21)
    85
    """

    prev_numerator = 1
    prev_denominator = 0

    numerator = 1
    denominator = 1

    while numerator <= 2 * min_total - 1:
        prev_numerator += 2 * numerator
        numerator += 2 * prev_numerator

        prev_denominator += 2 * denominator
        denominator += 2 * prev_denominator

    return (denominator + 1) // 2


if __name__ == "__main__":
    print(f"{solution() = }")
