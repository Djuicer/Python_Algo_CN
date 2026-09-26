def sliding_window(input_string: str) -> int:
    """
    接收一个字符串，使用滑动窗口（Sliding Window）算法
    返回不含重复字符的最长子串长度。

    时间复杂度为 O(n)，其中 n 为字符串长度。滑动窗口
    保证每个字符最多处理两次。

    参数：
        input_string：输入字符串。

    返回：
        int：不含重复字符的最长子串长度。

    异常：
        TypeError：输入不是字符串时抛出。

    示例：
    >>> sliding_window("abcabcbb")
    3
    >>> sliding_window("bbbbb")
    1
    >>> sliding_window("pwwkew")
    3
    >>> sliding_window("")
    0
    >>> sliding_window("abcdefg")
    7
    >>> sliding_window("abccba")
    3
    >>> sliding_window("a"*10000)
    1
    """
    # 处理非字符串输入
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    # 直接处理空字符串
    if len(input_string) == 0:
        return 0

    # 记录每个字符最近一次出现位置的字典
    char_index_map: dict[str, int] = {}

    # 初始化滑动窗口指针
    left: int = 0
    max_len: int = 0
    # 用右指针遍历字符串
    for right, char in enumerate(input_string):
        if char in char_index_map and char_index_map[char] >= left:
            # 移动左指针以避免重复字符
            left = char_index_map[char] + 1
        # 更新字符最近一次出现的索引
        char_index_map[char] = right
        # 计算当前窗口长度
        current_len = right - left + 1
        max_len = max(max_len, current_len)
    return max_len


if __name__ == "__main__":
    import doctest

    doctest.testmod()
