"""
Project Euler Problem 104 : https://projecteuler.net/problem=104

斐波那契数列由以下递推关系定义：

Fn = Fn-1 + Fn-2，其中 F1 = 1 且 F2 = 1。
事实证明，包含 113 位的 F541 是首个末九位为 1-9 全数字（包含数字 1 到 9，
顺序不限）的斐波那契数。包含 575 位的 F2749 是首个前九位为 1-9 全数字的斐波那契数。

已知 Fk 是首个前九位和末九位均为 1-9 全数字的斐波那契数，求 k。
"""

import sys

sys.set_int_max_str_digits(0)


def check(number: int) -> bool:
    """
    接收一个数，检查其首尾是否均为全数字。


    >>> check(123456789987654321)
    True

    >>> check(120000987654321)
    False

    >>> check(1234567895765677987654321)
    True

    """

    check_last = [0] * 11
    check_front = [0] * 11

    # 标记末 9 位数字
    for _ in range(9):
        check_last[int(number % 10)] = 1
        number = number // 10
    # 标志
    f = True

    # 检查末 9 位数字是否为全数字

    for x in range(9):
        if not check_last[x + 1]:
            f = False
    if not f:
        return f

    # 标记前 9 位数字
    number = int(str(number)[:9])

    for _ in range(9):
        check_front[int(number % 10)] = 1
        number = number // 10

    # 检查前 9 位数字是否为全数字

    for x in range(9):
        if not check_front[x + 1]:
            f = False
    return f


def check1(number: int) -> bool:
    """
    接收一个数，检查其末尾是否为全数字。

    >>> check1(123456789987654321)
    True

    >>> check1(120000987654321)
    True

    >>> check1(12345678957656779870004321)
    False

    """

    check_last = [0] * 11

    # 标记末 9 位数字
    for _ in range(9):
        check_last[int(number % 10)] = 1
        number = number // 10
    # 标志
    f = True

    # 检查末 9 位数字是否为全数字

    for x in range(9):
        if not check_last[x + 1]:
            f = False
    return f


def solution() -> int:
    """
    输出首尾均为全数字的最小斐波那契数所对应的答案。
    >>> solution()
    329468
    """

    a = 1
    b = 1
    c = 2
    # 临时斐波那契数

    a1 = 1
    b1 = 1
    c1 = 2
    # 对 1e9 取模后的临时斐波那契数

    # 对 m=1e9 取模，以加快计算
    tocheck = [0] * 1000000
    m = 1000000000

    for x in range(1000000):
        c1 = (a1 + b1) % m
        a1 = b1 % m
        b1 = c1 % m
        if check1(b1):
            tocheck[x + 3] = 1

    for x in range(1000000):
        c = a + b
        a = b
        b = c
        # 仅当索引位于 tocheck 中时执行检查
        if tocheck[x + 3] and check(b):
            return x + 3  # 前 2 项已处理
    return -1


if __name__ == "__main__":
    print(f"{solution() = }")
