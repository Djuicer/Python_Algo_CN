def decimal_to_negative_binary(number: int) -> int:
    """
    从十进制转换为负二进制（基数为 -2）的算法。

    https://en.wikipedia.org/wiki/Negative_base#:~:text=Binary-,Negabinary,-Ternary

    >>> decimal_to_negative_binary(10)
    11110
    >>> decimal_to_negative_binary(-10)
    1010
    >>> decimal_to_negative_binary(-30)
    100110
    >>> decimal_to_negative_binary(30)
    1100010
    """

    if number == 0:
        return 0
    result_str = ""
    while number != 0:
        number, remainder = divmod(number, -2)
        if remainder < 0:
            number, remainder = number + 1, remainder + 2
        result_str = str(remainder) + result_str
    return int(result_str)


if __name__ == "__main__":
    __import__("doctest").testmod()
