# Created by susmith98

from collections import Counter
from timeit import timeit

# 问题描述：
# 检查给定字符串的字符能否重新排列为回文。
# 长字符串使用 Counter 更快，短字符串不使用 Counter 更快。


def can_string_be_rearranged_as_palindrome_counter(
    input_str: str = "",
) -> bool:
    """
    回文（Palindrome）是正读与反读相同的字符串。
    回文示例：mom、dad、malayalam
    >>> can_string_be_rearranged_as_palindrome_counter("Momo")
    True
    >>> can_string_be_rearranged_as_palindrome_counter("Mother")
    False
    >>> can_string_be_rearranged_as_palindrome_counter("Father")
    False
    >>> can_string_be_rearranged_as_palindrome_counter("A man a plan a canal Panama")
    True
    """
    return sum(c % 2 for c in Counter(input_str.replace(" ", "").lower()).values()) < 2


def can_string_be_rearranged_as_palindrome(input_str: str = "") -> bool:
    """
    回文（Palindrome）是正读与反读相同的字符串。
    回文示例：mom、dad、malayalam
    >>> can_string_be_rearranged_as_palindrome("Momo")
    True
    >>> can_string_be_rearranged_as_palindrome("Mother")
    False
    >>> can_string_be_rearranged_as_palindrome("Father")
    False
    >>> can_string_be_rearranged_as_palindrome_counter("A man a plan a canal Panama")
    True
    """
    if len(input_str) == 0:
        return True
    lower_case_input_str = input_str.replace(" ", "").lower()
    # character_freq_dict: 保存输入字符串中每个字符的频次
    character_freq_dict: dict[str, int] = {}

    for character in lower_case_input_str:
        character_freq_dict[character] = character_freq_dict.get(character, 0) + 1
    """
    上面一行代码等价于：
    1) 获取截至前一个索引时当前字符的频次
    >>> character_freq =  character_freq_dict.get(character, 0)
    2) Incrementing the frequency of current character by 1
    >>> character_freq = character_freq + 1
    3) Updating the frequency of current character
    >>> character_freq_dict[character] = character_freq
    """
    """
    观察：
    偶数长度的回文
    -> 每个字符均出现偶数次。
    奇数长度的回文
    -> 除一个字符外，其余字符均出现偶数次。
    逻辑：
    第 1 步：统计出现奇数次的字符数量，即 oddChar
    第 2 步：若有超过一个字符出现奇数次，
    则无法重新排列为回文
    """
    odd_char = 0

    for character_count in character_freq_dict.values():
        if character_count % 2:
            odd_char += 1
    return not odd_char > 1


def benchmark(input_str: str = "") -> None:
    """
    比较上述两个函数的基准测试代码
    """
    print("\nFor string = ", input_str, ":")
    print(
        "> can_string_be_rearranged_as_palindrome_counter()",
        "\tans =",
        can_string_be_rearranged_as_palindrome_counter(input_str),
        "\ttime =",
        timeit(
            "z.can_string_be_rearranged_as_palindrome_counter(z.check_str)",
            setup="import __main__ as z",
        ),
        "seconds",
    )
    print(
        "> can_string_be_rearranged_as_palindrome()",
        "\tans =",
        can_string_be_rearranged_as_palindrome(input_str),
        "\ttime =",
        timeit(
            "z.can_string_be_rearranged_as_palindrome(z.check_str)",
            setup="import __main__ as z",
        ),
        "seconds",
    )


if __name__ == "__main__":
    check_str = input(
        "Enter string to determine if it can be rearranged as a palindrome or not: "
    ).strip()
    benchmark(check_str)
    status = can_string_be_rearranged_as_palindrome_counter(check_str)
    print(f"{check_str} can {'' if status else 'not '}be rearranged as a palindrome")
