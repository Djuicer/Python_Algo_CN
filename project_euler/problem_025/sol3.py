"""
斐波那契数列由以下递推关系定义：

    Fn = Fn-1 + Fn-2, where F1 = 1 and F2 = 1.

因此前 12 项为：

    F1 = 1
    F2 = 1
    F3 = 2
    F4 = 3
    F5 = 5
    F6 = 8
    F7 = 13
    F8 = 21
    F9 = 34
    F10 = 55
    F11 = 89
    F12 = 144

第 12 项 F12 是第一个包含三位数字的项。

斐波那契数列中第一个包含 1000 位数字的项，其索引是多少？
"""


def solution(n: int = 1000) -> int:
    """返回斐波那契数列中第一个包含 n 位数字的项的索引。

    >>> solution(1000)
    4782
    >>> solution(100)
    476
    >>> solution(50)
    237
    >>> solution(3)
    12
    """
    f1, f2 = 1, 1
    index = 2
    while True:
        i = 0
        f = f1 + f2
        f1, f2 = f2, f
        index += 1
        for _ in str(f):
            i += 1
        if i == n:
            break
    return index


if __name__ == "__main__":
    print(solution(int(str(input()).strip())))
