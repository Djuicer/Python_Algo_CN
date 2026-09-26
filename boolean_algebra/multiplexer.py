def mux(input0: int, input1: int, select: int) -> int:
    """
    实现二选一多路复用器（Multiplexer）。

    :param input0: 第一个输入值（0 或 1）。
    :param input1: 第二个输入值（0 或 1）。
    :param select: 用于在 input0 和 input1 之间选择的选择信号（0 或 1）。
    :return: 根据选择信号得到的输出，即 input1 if select else input0。

    https://www.electrically4u.com/solved-problems-on-multiplexer
    https://en.wikipedia.org/wiki/Multiplexer

    >>> mux(0, 1, 0)
    0
    >>> mux(0, 1, 1)
    1
    >>> mux(1, 0, 0)
    1
    >>> mux(1, 0, 1)
    0
    >>> mux(2, 1, 0)
    Traceback (most recent call last):
        ...
    ValueError: Inputs and select signal must be 0 or 1
    >>> mux(0, -1, 0)
    Traceback (most recent call last):
        ...
    ValueError: Inputs and select signal must be 0 or 1
    >>> mux(0, 1, 1.1)
    Traceback (most recent call last):
        ...
    ValueError: Inputs and select signal must be 0 or 1
    """
    if all(i in (0, 1) for i in (input0, input1, select)):
        return input1 if select else input0
    raise ValueError("Inputs and select signal must be 0 or 1")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
