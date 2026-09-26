def reverse_words(sentence: str) -> str:
    """反转给定字符串中单词的顺序。

    忽略单词间多余的空白字符。

    >>> reverse_words("I love Python")
    'Python love I'
    >>> reverse_words("I     Love          Python")
    'Python Love I'
    """
    return " ".join(sentence.split()[::-1])


if __name__ == "__main__":
    import doctest

    doctest.testmod()
