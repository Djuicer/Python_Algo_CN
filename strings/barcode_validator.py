"""
https://en.wikipedia.org/wiki/Check_digit#Algorithms
"""


def get_check_digit(barcode: int) -> int:
    """
    先去掉条形码的最后一位，
    再根据剩余的 12 位计算，
    返回实际应有的最后一位。

    >>> get_check_digit(8718452538119)
    9
    >>> get_check_digit(87184523)
    5
    >>> get_check_digit(87193425381086)
    9
    >>> [get_check_digit(x) for x in range(0, 100, 10)]
    [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]
    """
    barcode //= 10  # 去掉最后一位
    checker = False
    s = 0

    # 提取并检查每一位
    while barcode != 0:
        mult = 1 if checker else 3
        s += mult * (barcode % 10)
        barcode //= 10
        checker = not checker

    return (10 - (s % 10)) % 10


def is_valid(barcode: int) -> bool:
    """
    检查条形码长度及最后一位
    返回表示条形码是否有效的布尔值

    >>> is_valid(8718452538119)
    True
    >>> is_valid(87184525)
    False
    >>> is_valid(87193425381089)
    False
    >>> is_valid(0)
    False
    >>> is_valid(dwefgiweuf)
    Traceback (most recent call last):
        ...
    NameError: name 'dwefgiweuf' is not defined
    """
    return len(str(barcode)) == 13 and get_check_digit(barcode) == barcode % 10


def get_barcode(barcode: str) -> int:
    """
    以整数形式返回条形码

    >>> get_barcode("8718452538119")
    8718452538119
    >>> get_barcode("dwefgiweuf")
    Traceback (most recent call last):
        ...
    ValueError: Barcode 'dwefgiweuf' has alphabetic characters.
    """
    if str(barcode).isalpha():
        msg = f"Barcode '{barcode}' has alphabetic characters."
        raise ValueError(msg)
    if int(barcode) < 0:
        raise ValueError("The entered barcode has a negative value. Try again.")
    return int(barcode)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    """
    输入条形码。

    """
    barcode = get_barcode(input("Barcode: ").strip())

    if is_valid(barcode):
        print(f"'{barcode}' is a valid barcode.")
    else:
        print(f"'{barcode}' is NOT a valid barcode.")
