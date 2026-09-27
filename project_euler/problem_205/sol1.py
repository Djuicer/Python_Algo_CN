"""
Project Euler Problem 205: https://projecteuler.net/problem=205

Peter 有九个四面（正四面体）骰子，每个骰子的面编号为 1, 2, 3, 4。
Colin 有六个六面（立方体）骰子，每个骰子的面编号为 1, 2, 3, 4, 5, 6。

Peter 和 Colin 掷出骰子并比较总点数：总点数较高者获胜；若相等则为平局。

正四面体骰子的 Peter 击败立方体骰子的 Colin 的概率是多少？
将答案四舍五入到小数点后七位，并以 0.abcdefg 的形式给出。
"""

from itertools import product


def total_frequency_distribution(sides_number: int, dice_number: int) -> list[int]:
    """
    返回总点数的频数分布。

    >>> total_frequency_distribution(sides_number=6, dice_number=1)
    [0, 1, 1, 1, 1, 1, 1]

    >>> total_frequency_distribution(sides_number=4, dice_number=2)
    [0, 0, 1, 2, 3, 4, 3, 2, 1]
    """

    max_face_number = sides_number
    max_total = max_face_number * dice_number
    totals_frequencies = [0] * (max_total + 1)

    min_face_number = 1
    faces_numbers = range(min_face_number, max_face_number + 1)
    for dice_numbers in product(faces_numbers, repeat=dice_number):
        total = sum(dice_numbers)
        totals_frequencies[total] += 1

    return totals_frequencies


def solution() -> float:
    """
    返回正四面体骰子的 Peter 击败立方体骰子的 Colin 的概率，
    四舍五入到小数点后七位，并采用 0.abcdefg 的形式。

    >>> solution()
    0.5731441
    """

    peter_totals_frequencies = total_frequency_distribution(
        sides_number=4, dice_number=9
    )
    colin_totals_frequencies = total_frequency_distribution(
        sides_number=6, dice_number=6
    )

    peter_wins_count = 0
    min_peter_total = 9
    max_peter_total = 4 * 9
    min_colin_total = 6
    for peter_total in range(min_peter_total, max_peter_total + 1):
        peter_wins_count += peter_totals_frequencies[peter_total] * sum(
            colin_totals_frequencies[min_colin_total:peter_total]
        )

    total_games_number = (4**9) * (6**6)
    peter_win_probability = peter_wins_count / total_games_number

    rounded_peter_win_probability = round(peter_win_probability, ndigits=7)

    return rounded_peter_win_probability


if __name__ == "__main__":
    print(f"{solution() = }")
