def capitalize(sentence: str) -> str:
    """
    将句子或单词的首字母转为大写。

    >>> capitalize("hello world")
    'Hello world'
    >>> capitalize("123 hello world")
    '123 hello world'
    >>> capitalize(" hello world")
    ' hello world'
    >>> capitalize("a")
    'A'
    >>> capitalize("")
    ''
    """

    # 首字符为小写字母时，将其转为大写
    # 将大写首字符与字符串其余部分拼接
    # 切片使空字符串也能安全处理。
    return sentence[:1].upper() + sentence[1:]


if __name__ == "__main__":
    from doctest import testmod

    testmod()
