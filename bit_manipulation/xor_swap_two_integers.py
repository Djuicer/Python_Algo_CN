# 异或交换相关资料：https://en.wikipedia.org/wiki/Bitwise_operation#XOR

# 算法：
# 1. 接收两个整数 a 和 b。
# 2. 对 a 和 b 执行异或运算，并将结果存入 a：
#       a = a ^ b
# 3. 将 a 的新值与 b 异或，得到 a 的原值，并将其存入 b：
#       b = a ^ b
# 4. 将 a 的新值与 b 的新值异或，得到 b 的原值，并将其存入 a：
#       a = a ^ b
# 5. 返回交换后的值 (a, b)。
# 此方法无需使用临时变量即可交换两个数。


def xor_swap(a: int, b: int) -> tuple[int, int]:
    """
    使用按位异或运算交换两个整数，并返回交换后的值。

    >>> xor_swap(5, 10)
    (10, 5)
    >>> xor_swap(0, 0)
    (0, 0)
    >>> xor_swap(-1, 1)
    (1, -1)
    >>> xor_swap(123, 456)
    (456, 123)
    >>> xor_swap(12345, 54321)
    (54321, 12345)
    """
    a = a ^ b
    b = a ^ b
    a = a ^ b
    return a, b


if __name__ == "__main__":
    import doctest

    doctest.testmod()
