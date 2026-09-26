import re

"""
基本信息：
https://en.wikipedia.org/wiki/Naming_convention_(programming)#Python_and_Ruby

帕斯卡命名法（Pascal Case，即大驼峰命名法）：https://en.wikipedia.org/wiki/Camel_case

驼峰命名法（Camel Case）：https://en.wikipedia.org/wiki/Camel_case

短横线命名法（Kebab Case，参见基本信息）：
https://en.wikipedia.org/wiki/Naming_convention_(programming)#Python_and_Ruby

蛇形命名法（Snake Case）：https://en.wikipedia.org/wiki/Snake_case
"""


# 辅助函数
def split_input(str_: str) -> list:
    """
    >>> split_input("one two 31235three4four")
    [['one', 'two', '31235three4four']]
    """
    return [char.split() for char in re.split(r"[^ a-z A-Z 0-9 \s]", str_)]


def to_simple_case(str_: str) -> str:
    """
    >>> to_simple_case("one two 31235three4four")
    'OneTwo31235three4four'
    >>> to_simple_case("This should be combined")
    'ThisShouldBeCombined'
    >>> to_simple_case("The first letters are capitalized, then string is merged")
    'TheFirstLettersAreCapitalizedThenStringIsMerged'
    >>> to_simple_case("special characters :, ', %, ^, $, are ignored")
    'SpecialCharactersAreIgnored'
    """
    string_split = split_input(str_)
    return "".join(
        ["".join([char.capitalize() for char in sub_str]) for sub_str in string_split]
    )


def to_complex_case(text: str, upper: bool, separator: str) -> str:
    """
    返回使用指定分隔符连接后的字符串。

    Parameters:
    @text: 要执行操作的字符串
    @upper: 决定是否将结果转为大写的布尔值
    @separator: 连接单词所用的分隔符

    示例：
    >>> to_complex_case("one two 31235three4four", True, "_")
    'ONE_TWO_31235THREE4FOUR'
    >>> to_complex_case("one two 31235three4four", False, "-")
    'one-two-31235three4four'
    """
    try:
        string_split = split_input(text)
        if upper:
            res_str = "".join(
                [
                    separator.join([char.upper() for char in sub_str])
                    for sub_str in string_split
                ]
            )
        else:
            res_str = "".join(
                [
                    separator.join([char.lower() for char in sub_str])
                    for sub_str in string_split
                ]
            )
        return res_str
    except IndexError:
        return "not valid string"


# 主体内容
def to_pascal_case(text: str) -> str:
    """
    >>> to_pascal_case("one two 31235three4four")
    'OneTwo31235three4four'
    """
    return to_simple_case(text)


def to_camel_case(text: str) -> str:
    """
    >>> to_camel_case("one two 31235three4four")
    'oneTwo31235three4four'
    """
    try:
        res_str = to_simple_case(text)
        return res_str[0].lower() + res_str[1:]
    except IndexError:
        return "not valid string"


def to_snake_case(text: str, upper: bool) -> str:
    """
    >>> to_snake_case("one two 31235three4four", True)
    'ONE_TWO_31235THREE4FOUR'
    >>> to_snake_case("one two 31235three4four", False)
    'one_two_31235three4four'
    """
    return to_complex_case(text, upper, "_")


def to_kebab_case(text: str, upper: bool) -> str:
    """
    >>> to_kebab_case("one two 31235three4four", True)
    'ONE-TWO-31235THREE4FOUR'
    >>> to_kebab_case("one two 31235three4four", False)
    'one-two-31235three4four'
    """
    return to_complex_case(text, upper, "-")


if __name__ == "__main__":
    __import__("doctest").testmod()
