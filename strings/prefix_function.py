"""
https://cp-algorithms.com/string/prefix-function.html

Knuth-Morris-Pratt 算法中的前缀函数（Prefix Function）

与 Knuth-Morris-Pratt 模式查找算法不同

例如，查找同时也是后缀的最长前缀

时间复杂度：O(n)，其中 n 为字符串长度
"""


def prefix_function(input_string: str) -> list:
    """
    为给定字符串的每个索引 i 计算一个值，
    表示子串 input_str[0...i] 的前缀和后缀
    相同部分的最大长度

    第一个元素的值始终为 0

    >>> prefix_function("aabcdaabc")
    [0, 1, 0, 0, 0, 1, 2, 3, 4]
    >>> prefix_function("asdasdad")
    [0, 0, 0, 1, 2, 3, 4, 0]
    """

    # 保存结果值的列表
    prefix_result = [0] * len(input_string)

    for i in range(1, len(input_string)):
        # 使用先前结果提高性能，即动态规划
        j = prefix_result[i - 1]
        while j > 0 and input_string[i] != input_string[j]:
            j = prefix_result[j - 1]

        if input_string[i] == input_string[j]:
            j += 1
        prefix_result[i] = j

    return prefix_result


def longest_prefix(input_str: str) -> int:
    """
    前缀函数的应用
    查找同时也是后缀的最长前缀

    >>> longest_prefix("aabcdaabc")
    4
    >>> longest_prefix("asdasdad")
    4
    >>> longest_prefix("abcab")
    2
    """

    # 返回数组最大值即可得到答案
    return max(prefix_function(input_str))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
