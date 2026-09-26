"""
Fletcher 校验和是一种计算位置相关校验和的算法，由 John G. Fletcher
（1934—2012）于 20 世纪 70 年代末在劳伦斯利弗莫尔实验室提出。[1]
Fletcher 校验和旨在以求和技术较低的计算开销，提供接近循环冗余校验的
错误检测能力。

来源：https://en.wikipedia.org/wiki/Fletcher%27s_checksum
"""


def fletcher16(text: str) -> int:
    """
    遍历数据中的每个字符，并将其累加到两个和值中。

    >>> fletcher16('hello world')
    6752
    >>> fletcher16('onethousandfourhundredthirtyfour')
    28347
    >>> fletcher16('The quick brown fox jumps over the lazy dog.')
    5655
    """
    data = bytes(text, "ascii")
    sum1 = 0
    sum2 = 0
    for character in data:
        sum1 = (sum1 + character) % 255
        sum2 = (sum1 + sum2) % 255
    return (sum2 << 8) | sum1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
