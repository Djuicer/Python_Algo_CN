def strip(user_string: str, characters: str = " \t\n\r") -> str:
    """
    移除字符串首尾的指定字符（默认为空白字符）。

    参数：
        user_string (str): 待去除首尾字符的输入字符串。
        characters (str, optional): 可选的待移除字符
                （默认为空白字符）。

    返回：
        str: 去除首尾字符后的字符串。

    示例：
        >>> strip("   hello   ")
        'hello'
        >>> strip("...world...", ".")
        'world'
        >>> strip("123hello123", "123")
        'hello'
        >>> strip("")
        ''
    """

    start = 0
    end = len(user_string)

    while start < end and user_string[start] in characters:
        start += 1

    while end > start and user_string[end - 1] in characters:
        end -= 1

    return user_string[start:end]
