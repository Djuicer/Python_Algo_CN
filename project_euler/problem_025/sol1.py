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


def fibonacci(n: int) -> int:
    """
    通过迭代 n 个数并使用斐波那契公式创建整数数组，计算输入 n 对应的斐波那契数。
    返回数组的第 n 个元素。

    >>> fibonacci(2)
    1
    >>> fibonacci(3)
    2
    >>> fibonacci(5)
    5
    >>> fibonacci(10)
    55
    >>> fibonacci(12)
    144

    """
    if n == 1 or not isinstance(n, int):
        return 0
    elif n == 2:
        return 1
    else:
        sequence = [0, 1]
        for i in range(2, n + 1):
            sequence.append(sequence[i - 1] + sequence[i - 2])

        return sequence[n]


def fibonacci_digits_index(n: int) -> int:
    """
    从 3 开始依次计算斐波那契数，直到结果的位数等于输入值 n。
    返回此时对应的斐波那契数列项序号。

    >>> fibonacci_digits_index(1000)
    4782
    >>> fibonacci_digits_index(100)
    476
    >>> fibonacci_digits_index(50)
    237
    >>> fibonacci_digits_index(3)
    12
    """
    digits = 0
    index = 2

    while digits < n:
        index += 1
        digits = len(str(fibonacci(index)))

    return index


def solution(n: int = 1000) -> int:
    """
    返回斐波那契数列中第一个包含 n 位数字的项的索引。

    >>> solution(1000)
    4782
    >>> solution(100)
    476
    >>> solution(50)
    237
    >>> solution(3)
    12
    """
    return fibonacci_digits_index(n)


if __name__ == "__main__":
    print(solution(int(str(input()).strip())))
