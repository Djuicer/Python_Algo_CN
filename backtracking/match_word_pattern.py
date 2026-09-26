def match_word_pattern(pattern: str, input_string: str) -> bool:
    """
    使用回溯法判断给定模式是否与字符串匹配。

    pattern: 待匹配的模式。
    input_string: 要与模式匹配的字符串。
    return: 模式与字符串匹配时返回 True，否则返回 False。

    >>> match_word_pattern("aba", "GraphTreesGraph")
    True

    >>> match_word_pattern("xyx", "PythonRubyPython")
    True

    >>> match_word_pattern("GG", "PythonJavaPython")
    False
    """

    def backtrack(pattern_index: int, str_index: int) -> bool:
        """
        >>> backtrack(0, 0)
        True

        >>> backtrack(0, 1)
        True

        >>> backtrack(0, 4)
        False
        """
        if pattern_index == len(pattern) and str_index == len(input_string):
            return True
        if pattern_index == len(pattern) or str_index == len(input_string):
            return False
        char = pattern[pattern_index]
        if char in pattern_map:
            mapped_str = pattern_map[char]
            if input_string.startswith(mapped_str, str_index):
                return backtrack(pattern_index + 1, str_index + len(mapped_str))
            else:
                return False
        for end in range(str_index + 1, len(input_string) + 1):
            substr = input_string[str_index:end]
            if substr in str_map:
                continue
            pattern_map[char] = substr
            str_map[substr] = char
            if backtrack(pattern_index + 1, end):
                return True
            del pattern_map[char]
            del str_map[substr]
        return False

    pattern_map: dict[str, str] = {}
    str_map: dict[str, str] = {}
    return backtrack(0, 0)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
