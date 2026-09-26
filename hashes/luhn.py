"""Luhn 算法。"""

from __future__ import annotations


def is_luhn(string: str) -> bool:
    """
    对输入字符串执行 Luhn 校验。
    算法：
    * 从倒数第二位起，每隔一位将数字加倍。
    * 若数字大于 9，则减去 9。
    * 对所有数字求和。
    *
    >>> test_cases = (79927398710, 79927398711, 79927398712, 79927398713,
    ...     79927398714, 79927398715, 79927398716, 79927398717, 79927398718,
    ...     79927398719)
    >>> [is_luhn(str(test_case)) for test_case in test_cases]
    [False, False, False, True, False, False, False, False, False, False]
    """
    check_digit: int
    _vector: list[str] = list(string)
    __vector, check_digit = _vector[:-1], int(_vector[-1])
    vector: list[int] = [int(digit) for digit in __vector]

    vector.reverse()
    for i, digit in enumerate(vector):
        if i & 1 == 0:
            doubled: int = digit * 2
            if doubled > 9:
                doubled -= 9
            check_digit += doubled
        else:
            check_digit += digit

    return check_digit % 10 == 0


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    assert is_luhn("79927398713")
    assert not is_luhn("79927398714")
