"""
培根密码（Baconian Cipher，又称 Bacon's Cipher）的编码与解码程序。
维基百科参考资料：https://en.wikipedia.org/wiki/Bacon%27s_cipher
"""

encode_dict = {
    "a": "AAAAA",
    "b": "AAAAB",
    "c": "AAABA",
    "d": "AAABB",
    "e": "AABAA",
    "f": "AABAB",
    "g": "AABBA",
    "h": "AABBB",
    "i": "ABAAA",
    "j": "BBBAA",
    "k": "ABAAB",
    "l": "ABABA",
    "m": "ABABB",
    "n": "ABBAA",
    "o": "ABBAB",
    "p": "ABBBA",
    "q": "ABBBB",
    "r": "BAAAA",
    "s": "BAAAB",
    "t": "BAABA",
    "u": "BAABB",
    "v": "BBBAB",
    "w": "BABAA",
    "x": "BABAB",
    "y": "BABBA",
    "z": "BABBB",
    " ": " ",
}


decode_dict = {value: key for key, value in encode_dict.items()}


def encode(word: str) -> str:
    """
    编码为培根密码。

    >>> encode("hello")
    'AABBBAABAAABABAABABAABBAB'
    >>> encode("hello world")
    'AABBBAABAAABABAABABAABBAB BABAAABBABBAAAAABABAAAABB'
    >>> encode("hello world!")
    Traceback (most recent call last):
        ...
    Exception: encode() accepts only letters of the alphabet and spaces
    """
    encoded = ""
    for letter in word.lower():
        if letter.isalpha() or letter == " ":
            encoded += encode_dict[letter]
        else:
            raise Exception("encode() accepts only letters of the alphabet and spaces")
    return encoded


def decode(coded: str) -> str:
    """
    解码培根密码。

    >>> decode("AABBBAABAAABABAABABAABBAB BABAAABBABBAAAAABABAAAABB")
    'hello world'
    >>> decode("AABBBAABAAABABAABABAABBAB")
    'hello'
    >>> decode("AABBBAABAAABABAABABAABBAB BABAAABBABBAAAAABABAAAABB!")
    Traceback (most recent call last):
        ...
    Exception: decode() accepts only 'A', 'B' and spaces
    """
    if set(coded) - {"A", "B", " "} != set():
        raise Exception("decode() accepts only 'A', 'B' and spaces")
    decoded = ""
    for word in coded.split():
        while len(word) != 0:
            decoded += decode_dict[word[:5]]
            word = word[5:]
        decoded += " "
    return decoded.strip()


if __name__ == "__main__":
    from doctest import testmod

    testmod()
