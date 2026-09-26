def upper(word: str) -> str:
    """
    查找字符串中的 ASCII 小写字母，将其整数表示减去 32，
    得到对应的大写字母，从而将整个字符串中的
    ASCII 字母转为大写。

    >>> upper("wow")
    'WOW'
    >>> upper("Hello")
    'HELLO'
    >>> upper("WHAT")
    'WHAT'
    >>> upper("wh[]32")
    'WH[]32'
    """
    return "".join(chr(ord(char) - 32) if "a" <= char <= "z" else char for char in word)


if __name__ == "__main__":
    from doctest import testmod

    testmod()
