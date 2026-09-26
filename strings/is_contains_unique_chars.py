def is_contains_unique_chars(input_str: str) -> bool:
    """
    检查字符串中的字符是否全部互不相同。
    >>> is_contains_unique_chars("I_love.py")
    True
    >>> is_contains_unique_chars("I don't love Python")
    False

    时间复杂度：O(n)
    空间复杂度：O(1)，Unicode 中有 144697 个字符时占用 19320 字节
    """

    # 每一位表示一个 Unicode 字符
    # 例如，第 65 位表示 'A'
    # https://stackoverflow.com/a/12811293
    bitmap = 0
    for ch in input_str:
        ch_unicode = ord(ch)
        ch_bit_index_on = pow(2, ch_unicode)

        # 如果当前字符的 Unicode 对应位已经被置为 1
        if bitmap >> ch_unicode & 1 == 1:
            return False
        bitmap |= ch_bit_index_on
    return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()
