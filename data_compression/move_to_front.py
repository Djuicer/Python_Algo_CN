"""
前移变换（Move-to-front Transform）。

前移变换将每个符号编码为其在有序字母表中的当前索引，然后将该符号移到
字母表最前端。它通常用于无损压缩流程中的 Burrows-Wheeler 变换之后。

参考资料：https://en.wikipedia.org/wiki/Move-to-front_transform
"""


def _validated_alphabet(alphabet: str) -> list[str]:
    """
    验证字符唯一性后，返回可变的字母表列表。

    >>> _validated_alphabet("abc")
    ['a', 'b', 'c']
    >>> _validated_alphabet("aba")
    Traceback (most recent call last):
        ...
    ValueError: alphabet must contain unique characters
    """
    if not isinstance(alphabet, str):
        raise TypeError("alphabet must be a string")
    if len(set(alphabet)) != len(alphabet):
        raise ValueError("alphabet must contain unique characters")
    return list(alphabet)


def move_to_front_encode(text: str, alphabet: str) -> list[int]:
    """
    使用前移变换编码文本。

    >>> move_to_front_encode("banana", "abcdefghijklmnopqrstuvwxyz")
    [1, 1, 13, 1, 1, 1]
    >>> move_to_front_encode("banana", "abn")
    [1, 1, 2, 1, 1, 1]
    >>> move_to_front_encode("", "abc")
    []
    >>> move_to_front_encode("bad", "abc")
    Traceback (most recent call last):
        ...
    ValueError: character 'd' is not in the alphabet
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    symbols = _validated_alphabet(alphabet)
    encoded_text: list[int] = []

    for char in text:
        try:
            char_index = symbols.index(char)
        except ValueError:
            message = f"character {char!r} is not in the alphabet"
            raise ValueError(message) from None
        encoded_text.append(char_index)
        symbols.insert(0, symbols.pop(char_index))

    return encoded_text


def move_to_front_decode(encoded_text: list[int], alphabet: str) -> str:
    """
    解码经过前移变换编码的索引列表。

    >>> move_to_front_decode([1, 1, 13, 1, 1, 1], "abcdefghijklmnopqrstuvwxyz")
    'banana'
    >>> move_to_front_decode([1, 1, 2, 1, 1, 1], "abn")
    'banana'
    >>> move_to_front_decode([], "abc")
    ''
    >>> move_to_front_decode([3], "abc")
    Traceback (most recent call last):
        ...
    ValueError: index 3 is not valid for alphabet size 3
    >>> move_to_front_decode([-1], "abc")
    Traceback (most recent call last):
        ...
    ValueError: index -1 is not valid for alphabet size 3
    """
    symbols = _validated_alphabet(alphabet)
    decoded_text = []

    for index in encoded_text:
        if not 0 <= index < len(symbols):
            message = f"index {index} is not valid for alphabet size {len(symbols)}"
            raise ValueError(message)
        decoded_text.append(symbols[index])
        symbols.insert(0, symbols.pop(index))

    return "".join(decoded_text)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
