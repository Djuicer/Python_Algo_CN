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

from collections.abc import Generator


def fibonacci_generator() -> Generator[int]:
    """
    生成斐波那契数列中各项的生成器。

    >>> generator = fibonacci_generator()
    >>> next(generator)
    1
    >>> next(generator)
    2
    >>> next(generator)
    3
    >>> next(generator)
    5
    >>> next(generator)
    8
    """
    a, b = 0, 1
    while True:
        a, b = b, a + b
        yield b


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
    answer = 1
    gen = fibonacci_generator()
    while len(str(next(gen))) < n:
        answer += 1
    return answer + 1


if __name__ == "__main__":
    print(solution(int(str(input()).strip())))
