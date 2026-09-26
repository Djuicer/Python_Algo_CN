def split(string: str, separator: str = " ") -> list:
    """
    按分隔符拆分字符串，返回所有片段
    （默认按空格拆分）

    >>> split("apple#banana#cherry#orange",separator='#')
    ['apple', 'banana', 'cherry', 'orange']

    >>> split("Hello there")
    ['Hello', 'there']

    >>> split("11/22/63",separator = '/')
    ['11', '22', '63']

    >>> split("12:43:39",separator = ":")
    ['12', '43', '39']

    >>> split(";abbb;;c;", separator=';')
    ['', 'abbb', '', 'c', '']

    >>> split("a--b--c", separator="--")
    ['a', 'b', 'c']

    >>> split("apple##banana##cherry", separator="##")
    ['apple', 'banana', 'cherry']
    """

    split_words = []
    separator_length = len(separator)

    if separator_length == 0:
        return [string]

    last_index = 0
    index = 0
    while index < len(string):
        if string[index : index + separator_length] == separator:
            split_words.append(string[last_index:index])
            last_index = index + separator_length
            index += separator_length
        else:
            index += 1

    split_words.append(string[last_index:])
    return split_words


if __name__ == "__main__":
    from doctest import testmod

    testmod()
