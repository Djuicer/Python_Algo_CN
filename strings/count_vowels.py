def count_vowels(s: str) -> int:
    """
    统计给定字符串中的元音数量。

    :param s: 待统计元音的输入字符串。
    :return: 输入字符串中的元音数量。

    示例：
    >>> count_vowels("hello world")
    3
    >>> count_vowels("HELLO WORLD")
    3
    >>> count_vowels("123 hello world")
    3
    >>> count_vowels("")
    0
    >>> count_vowels("a quick brown fox")
    5
    >>> count_vowels("the quick BROWN fox")
    5
    >>> count_vowels("PYTHON")
    1
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")

    vowels = "aeiouAEIOU"
    return sum(1 for char in s if char in vowels)


if __name__ == "__main__":
    from doctest import testmod

    testmod()
