def hamming_distance(string1: str, string2: str) -> int:
    """计算两个等长字符串之间的汉明距离（Hamming Distance）
    在信息论中，两个等长字符串的汉明距离
    是对应位置的符号
    不同的位置数。https://en.wikipedia.org/wiki/Hamming_distance

    Args:
        string1 (str): 序列 1
        string2 (str): 序列 2

    Returns:
        int: 汉明距离

    >>> hamming_distance("python", "python")
    0
    >>> hamming_distance("karolin", "kathrin")
    3
    >>> hamming_distance("00000", "11111")
    5
    >>> hamming_distance("karolin", "kath")
    Traceback (most recent call last):
      ...
    ValueError: String lengths must match!
    """
    if len(string1) != len(string2):
        raise ValueError("String lengths must match!")

    count = 0

    for char1, char2 in zip(string1, string2):
        if char1 != char2:
            count += 1

    return count


if __name__ == "__main__":
    import doctest

    doctest.testmod()
