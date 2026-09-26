"""
使用分隔符连接字符串列表的程序
"""


def join(separator: str, separated: list[str]) -> str:
    """
    使用分隔符连接字符串列表，
    并返回结果。

    :param separator: 用于连接字符串的
                分隔符。
    :param separated: 待连接的字符串列表。

    :return: 使用指定分隔符连接后的字符串。

    示例：

    >>> join("", ["a", "b", "c", "d"])
    'abcd'
    >>> join("#", ["a", "b", "c", "d"])
    'a#b#c#d'
    >>> join("#", "a")
    'a'
    >>> join(" ", ["You", "are", "amazing!"])
    'You are amazing!'
    >>> join(",", ["", "", ""])
    ',,'

    此示例应对非字符串元素
    抛出异常：
    >>> join("#", ["a", "b", "c", 1])
    Traceback (most recent call last):
        ...
    Exception: join() accepts only strings

    使用不同分隔符的额外测试用例：
    >>> join("-", ["apple", "banana", "cherry"])
    'apple-banana-cherry'
    """

    # 检查所有元素是否为字符串
    for word_or_phrase in separated:
        # 元素不是字符串时抛出异常
        if not isinstance(word_or_phrase, str):
            raise Exception("join() accepts only strings")

    joined: str = ""
    """
    列表的最后一个元素之后没有分隔符。
    因此，遍历列表时，需要将最后一个元素之外的
    各元素与分隔符连接。
    """
    last_index: int = len(separated) - 1
    """
    遍历列表，将各元素与分隔符连接。
    除最后一个元素外，其他元素之后均有分隔符。
    """
    for word_or_phrase in separated[:last_index]:
        # 使用分隔符连接元素。
        joined += word_or_phrase + separator

    # 列表非空时连接最后一个元素。
    if separated != []:
        joined += separated[last_index]

    # 返回连接后的字符串。
    return joined


if __name__ == "__main__":
    from doctest import testmod

    testmod()
