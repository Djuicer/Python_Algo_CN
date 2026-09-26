"""
将字符串转换为数字序列，每个数字对应字符在字母表中的位置。

https://www.dcode.fr/letter-number-cipher
http://bestcodes.weebly.com/a1z26.html
"""

from __future__ import annotations


def encode(plain: str) -> list[int]:
    """
    >>> encode("myname")
    [13, 25, 14, 1, 13, 5]
    >>> encode("abCd")
    Traceback (most recent call last):
        ...
    ValueError: plain must contain only lowercase letters (a-z)
    >>> encode("n0w")
    Traceback (most recent call last):
        ...
    ValueError: plain must contain only lowercase letters (a-z)
    >>> encode("later!")
    Traceback (most recent call last):
        ...
    ValueError: plain must contain only lowercase letters (a-z)
    """
    if not plain.islower() or not plain.isalpha():
        raise ValueError("plain must contain only lowercase letters (a-z)")
    return [ord(elem) - 96 for elem in plain]


def decode(encoded: list[int]) -> str:
    """
    >>> decode([13, 25, 14, 1, 13, 5])
    'myname'
    """
    return "".join(chr(elem + 96) for elem in encoded)


def main() -> None:
    encoded = encode(input("-> ").strip().lower())
    print("Encoded: ", encoded)
    print("Decoded:", decode(encoded))


if __name__ == "__main__":
    main()
