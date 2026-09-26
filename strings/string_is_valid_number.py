"""
主题：确定有限自动机（Deterministic Finite Automaton，DFA）
给定字符串 s，判断它是否表示有效数值
LeetCode 链接：https://leetcode.com/problems/valid-number/description/
"""

from enum import Enum


class CharType(Enum):
    NUMERIC = "NUMERIC"
    SIGN = "SIGN"
    EXPONENT = "EXPONENT"
    DECIMAL = "DECIMAL"


class State(Enum):
    INITIAL = "INITIAL"
    SIGNED = "SIGNED"
    WHOLE = "WHOLE"
    FRACTIONAL = "FRACTIONAL"
    FRACTION = "FRACTION"
    EXPONENTIAL = "EXPONENTIAL"
    EXP_SIGN = "EXP_SIGN"
    EXP_NUMBER = "EXP_NUMBER"


state_machine: dict[State, dict[CharType, State]] = {
    State.INITIAL: {
        CharType.NUMERIC: State.WHOLE,
        CharType.SIGN: State.SIGNED,
        CharType.DECIMAL: State.FRACTIONAL,
    },
    State.SIGNED: {CharType.NUMERIC: State.WHOLE, CharType.DECIMAL: State.FRACTIONAL},
    State.WHOLE: {
        CharType.NUMERIC: State.WHOLE,
        CharType.DECIMAL: State.FRACTION,
        CharType.EXPONENT: State.EXPONENTIAL,
    },
    State.FRACTIONAL: {CharType.NUMERIC: State.FRACTION},
    State.FRACTION: {
        CharType.NUMERIC: State.FRACTION,
        CharType.EXPONENT: State.EXPONENTIAL,
    },
    State.EXPONENTIAL: {
        CharType.NUMERIC: State.EXP_NUMBER,
        CharType.SIGN: State.EXP_SIGN,
    },
    State.EXP_SIGN: {CharType.NUMERIC: State.EXP_NUMBER},
    State.EXP_NUMBER: {CharType.NUMERIC: State.EXP_NUMBER},
}


def classify_char(char: str) -> CharType | None:
    """
    将字符划分为以下类别之一：

    - 'CharType.NUMERIC': 数字（0-9）
    - 'CharType.SIGN': 加号（+）或减号（-）
    - 'CharType.EXPONENT': 'e' 或 'E'
        （用于指数记法）
    - 'CharType.DECIMAL': 小数点（.）
    - None: 不属于上述任何类别
    - None: char 的长度不为 1

    参数：
    char (str): 待分类的字符

    返回：
    CharType: 字符所属类别

    >>> classify_char('2')
    <CharType.NUMERIC: 'NUMERIC'>
    >>> classify_char('-')
    <CharType.SIGN: 'SIGN'>
    >>> classify_char('e')
    <CharType.EXPONENT: 'EXPONENT'>
    >>> classify_char('.')
    <CharType.DECIMAL: 'DECIMAL'>
    >>> classify_char('')

    >>> classify_char('0')
    <CharType.NUMERIC: 'NUMERIC'>
    >>> classify_char('01')
    """
    if len(char) != 1:
        return None
    if char.isdigit():
        return CharType.NUMERIC
    if char in "+-":
        return CharType.SIGN
    if char in "eE":
        return CharType.EXPONENT
    if char == ".":
        return CharType.DECIMAL
    return None


def is_valid_number(number_string: str) -> bool:
    """
    检查输入字符串是否表示有效数值。
    使用有限状态机解析输入字符串，
    根据字符类型在状态之间转移。
    若输入字符串表示有效数值，则返回 True，
    否则返回 False。
    有效数值指可以解析为整数、小数或
    指数形式的字符串。
    >>> is_valid_number("2")
    True
    >>> is_valid_number("0089")
    True
    >>> is_valid_number("-0.1")
    True
    >>> is_valid_number("+3.14")
    True
    >>> is_valid_number("4.")
    True
    >>> is_valid_number("-.9")
    True
    >>> is_valid_number("2e10")
    True
    >>> is_valid_number("-90E3")
    True
    >>> is_valid_number("3e+7")
    True
    >>> is_valid_number("+6e-1")
    True
    >>> is_valid_number("53.5e93")
    True
    >>> is_valid_number("-123.456e789")
    True


    >>> is_valid_number("abc")
    False
    >>> is_valid_number("1a")
    False
    >>> is_valid_number("1e")
    False
    >>> is_valid_number("e3")
    False
    >>> is_valid_number("99e2.5")
    False
    >>> is_valid_number("--6")
    False
    >>> is_valid_number("-+3")
    False
    >>> is_valid_number("95a54e53")
    False
    >>> is_valid_number(".")
    False
    """

    valid_final_states = {State.WHOLE, State.FRACTION, State.EXP_NUMBER}
    current_state = State.INITIAL

    for char in number_string:
        char_type = classify_char(char)
        if char_type is None or char_type not in state_machine[current_state]:
            return False
        current_state = state_machine[current_state][char_type]

    return current_state in valid_final_states


if __name__ == "__main__":
    import doctest

    doctest.testmod()
