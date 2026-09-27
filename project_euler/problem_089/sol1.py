"""
Project Euler Problem 89: https://projecteuler.net/problem=89

要使以罗马数字写成的数有效，必须遵循一些基本规则。尽管这些规则允许某些数字有
多种表示方式，但每个特定数字总有一种“最佳”写法。

例如，数字十六似乎至少有六种写法：

IIIIIIIIIIIIIIII
VIIIIIIIIIII
VVIIIIII
XIIIIII
VVVI
XVI

然而，根据规则只有 XIIIIII 和 XVI 有效，最后一种写法使用的数字字符最少，
因此被认为最高效。

11K 文本文件 roman.txt（右键单击并选择 'Save Link/Target As...'）包含一千个以有效但
不一定最简的罗马数字写成的数；本题的完整规则请参阅 About... Roman Numerals。

求将每个数字改写为最简形式后节省的字符数。

注意：可以假定文件中的所有罗马数字都不包含超过四个连续相同单位。
"""

import os

SYMBOLS = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def parse_roman_numerals(numerals: str) -> int:
    """
    将罗马数字字符串转换为整数。
    例如：
    >>> parse_roman_numerals("LXXXIX")
    89
    >>> parse_roman_numerals("IIII")
    4
    """

    total_value = 0

    index = 0
    while index < len(numerals) - 1:
        current_value = SYMBOLS[numerals[index]]
        next_value = SYMBOLS[numerals[index + 1]]
        if current_value < next_value:
            total_value -= current_value
        else:
            total_value += current_value
        index += 1
    total_value += SYMBOLS[numerals[index]]

    return total_value


def generate_roman_numerals(num: int) -> str:
    """
    为给定整数生成罗马数字字符串。
    例如：
    >>> generate_roman_numerals(89)
    'LXXXIX'
    >>> generate_roman_numerals(4)
    'IV'
    """

    numerals = ""

    m_count = num // 1000
    numerals += m_count * "M"
    num %= 1000

    c_count = num // 100
    if c_count == 9:
        numerals += "CM"
        c_count -= 9
    elif c_count == 4:
        numerals += "CD"
        c_count -= 4
    if c_count >= 5:
        numerals += "D"
        c_count -= 5
    numerals += c_count * "C"
    num %= 100

    x_count = num // 10
    if x_count == 9:
        numerals += "XC"
        x_count -= 9
    elif x_count == 4:
        numerals += "XL"
        x_count -= 4
    if x_count >= 5:
        numerals += "L"
        x_count -= 5
    numerals += x_count * "X"
    num %= 10

    if num == 9:
        numerals += "IX"
        num -= 9
    elif num == 4:
        numerals += "IV"
        num -= 4
    if num >= 5:
        numerals += "V"
        num -= 5
    numerals += num * "I"

    return numerals


def solution(roman_numerals_filename: str = "/p089_roman.txt") -> int:
    """
    计算并返回 Project Euler 第 89 题的答案。

    >>> solution("/numeralcleanup_test.txt")
    16
    """

    savings = 0

    with open(os.path.dirname(__file__) + roman_numerals_filename) as file1:
        lines = file1.readlines()

    for line in lines:
        original = line.strip()
        num = parse_roman_numerals(original)
        shortened = generate_roman_numerals(num)
        savings += len(original) - len(shortened)

    return savings


if __name__ == "__main__":
    print(f"{solution() = }")
