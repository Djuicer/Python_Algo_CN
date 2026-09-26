"""
https://cp-algorithms.com/string/z-function.html

Z 函数（Z-function），又称 Z 算法

高效查找模式在字符串中出现位置的算法

时间复杂度：O(n)，其中 n 为字符串长度

"""


def z_function(input_str: str) -> list[int]:
    """
    为给定字符串的每个索引计算一个值，
    表示从该索引开始、与同长度前缀相同的
    最长子串长度

    例如，对于字符串 'abab'，索引 2 处的值为 2

    第一个元素的值始终为 0

    >>> z_function("abracadabra")
    [0, 0, 0, 1, 0, 1, 0, 4, 0, 0, 1]
    >>> z_function("aaaa")
    [0, 3, 2, 1]
    >>> z_function("zxxzxxz")
    [0, 0, 0, 4, 0, 0, 1]
    """
    z_result = [0 for i in range(len(input_str))]

    # 初始化区间的左右指针
    left_pointer, right_pointer = 0, 0

    for i in range(1, len(input_str)):
        # 当前索引位于区间内部时
        if i <= right_pointer:
            min_edge = min(right_pointer - i + 1, z_result[i - left_pointer])
            z_result[i] = min_edge

        while go_next(i, z_result, input_str):
            z_result[i] += 1

        # 若新索引的结果使区间右端延伸得更远，
        # 则更新 left_pointer 和 right_pointer
        if i + z_result[i] - 1 > right_pointer:
            left_pointer, right_pointer = i, i + z_result[i] - 1

    return z_result


def go_next(i: int, z_result: list[int], s: str) -> bool:
    """
    检查是否需要继续比较下一个字符
    """
    return i + z_result[i] < len(s) and s[z_result[i]] == s[i + z_result[i]]


def find_pattern(pattern: str, input_str: str) -> int:
    """
    使用 Z 函数查找模式出现次数的示例
    返回 'pattern' 作为子串在
    'input_str' 中出现的次数

    >>> find_pattern("abr", "abracadabra")
    2
    >>> find_pattern("a", "aaaa")
    4
    >>> find_pattern("xz", "zxxzxxz")
    2
    >>> find_pattern("aa", "a")
    0
    """
    pattern_length = len(pattern)
    # 拼接 'pattern' 和 'input_str'，并对
    # 拼接后的字符串调用 z_function
    z_result = z_function(pattern + input_str)

    return sum(value >= pattern_length for value in z_result[pattern_length:])


if __name__ == "__main__":
    import doctest

    doctest.testmod()
