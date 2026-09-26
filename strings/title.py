def to_title_case(word: str) -> str:
    """
    将字符串转换为首字母大写形式，并保持输入内容不变。

    >>> to_title_case("Aakash")
    'Aakash'

    >>> to_title_case("aakash")
    'Aakash'

    >>> to_title_case("AAKASH")
    'Aakash'

    >>> to_title_case("aAkAsH")
    'Aakash'
    """

    """
    首字符为小写时，将其转为大写
    """
    if "a" <= word[0] <= "z":
        word = chr(ord(word[0]) - 32) + word[1:]

    """
    其余字符为大写时，将其转为小写
    """
    for i in range(1, len(word)):
        if "A" <= word[i] <= "Z":
            word = word[:i] + chr(ord(word[i]) + 32) + word[i + 1 :]

    return word


def sentence_to_title_case(input_str: str) -> str:
    """
    将字符串转换为标题格式，并保持输入内容不变。

    >>> sentence_to_title_case("Aakash Giri")
    'Aakash Giri'

    >>> sentence_to_title_case("aakash giri")
    'Aakash Giri'

    >>> sentence_to_title_case("AAKASH GIRI")
    'Aakash Giri'

    >>> sentence_to_title_case("aAkAsH gIrI")
    'Aakash Giri'
    """

    return " ".join(to_title_case(word) for word in input_str.split())


if __name__ == "__main__":
    from doctest import testmod

    testmod()
