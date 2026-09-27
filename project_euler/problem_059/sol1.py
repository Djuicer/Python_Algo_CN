"""
计算机中的每个字符都被分配一个唯一编码，首选标准是 ASCII
（American Standard Code for Information Interchange）。
例如，大写 A = 65、星号 (*) = 42、小写 k = 107。

一种现代加密方法是读取文本文件，将字节转换为 ASCII，然后让每个字节与取自密钥的
给定值进行 XOR。XOR 的优点是，对密文使用同一密钥即可恢复明文；例如，
65 XOR 42 = 107，然后 107 XOR 42 = 65。

对于不可破解的加密，密钥与明文消息等长，并由随机字节组成。用户会将加密消息和密钥
存放在不同位置；如果不能同时取得这两个“部分”，就无法解密消息。

遗憾的是，这种方法对大多数用户并不实用，因此改用密码作为密钥。如果密码比消息短，
就让密钥在整条消息中循环重复。该方法需要在安全性与可记忆性之间权衡：密码密钥既要
足够长，又要短到便于记忆。

本题已降低难度，因为加密密钥由三个小写字符组成。使用包含加密 ASCII 编码的文件
p059_cipher.txt（右键单击并选择 'Save Link/Target As...'），并利用明文必然包含
常见英语单词这一信息，解密消息并求原始文本中 ASCII 值的总和。
"""

from __future__ import annotations

import string
from itertools import cycle, product
from pathlib import Path

VALID_CHARS: str = (
    string.ascii_letters + string.digits + string.punctuation + string.whitespace
)
LOWERCASE_INTS: list[int] = [ord(letter) for letter in string.ascii_lowercase]
VALID_INTS: set[int] = {ord(char) for char in VALID_CHARS}

COMMON_WORDS: list[str] = ["the", "be", "to", "of", "and", "in", "that", "have"]


def try_key(ciphertext: list[int], key: tuple[int, ...]) -> str | None:
    """
    给定一条加密消息和一个可能的 3 字符密钥，解密该消息。
    如果解密消息包含无效字符，即不是 ASCII 字母、数字、标点或空白字符，
    则说明密钥错误，返回 None。
    >>> try_key([0, 17, 20, 4, 27], (104, 116, 120))
    'hello'
    >>> try_key([68, 10, 300, 4, 27], (104, 116, 120)) is None
    True
    """
    decoded: str = ""
    keychar: int
    cipherchar: int
    decodedchar: int

    for keychar, cipherchar in zip(cycle(key), ciphertext):
        decodedchar = cipherchar ^ keychar
        if decodedchar not in VALID_INTS:
            return None
        decoded += chr(decodedchar)

    return decoded


def filter_valid_chars(ciphertext: list[int]) -> list[str]:
    """
    给定一条加密消息，测试所有 3 字符字符串以尝试找出密钥。
    返回可能的解密消息列表。
    >>> from itertools import cycle
    >>> text = "The enemy's gate is down"
    >>> key = "end"
    >>> encoded = [ord(k) ^ ord(c) for k,c in zip(cycle(key), text)]
    >>> text in filter_valid_chars(encoded)
    True
    """
    possibles: list[str] = []
    for key in product(LOWERCASE_INTS, repeat=3):
        encoded = try_key(ciphertext, key)
        if encoded is not None:
            possibles.append(encoded)
    return possibles


def filter_common_word(possibles: list[str], common_word: str) -> list[str]:
    """
    给定可能的解码消息列表，通过检查指定常用词来缩小范围。
    仅返回包含 common_word 的解码消息。
    >>> filter_common_word(['asfla adf', 'I am here', '   !?! #a'], 'am')
    ['I am here']
    >>> filter_common_word(['athla amf', 'I am here', '   !?! #a'], 'am')
    ['athla amf', 'I am here']
    """
    return [possible for possible in possibles if common_word in possible.lower()]


def solution(filename: str = "p059_cipher.txt") -> int:
    """
    使用所有可能的 3 字符密钥测试密文，再用常用词筛选以缩小范围，
    直到只剩一条可能的解码消息。
    >>> solution("test_cipher.txt")
    3000
    """
    ciphertext: list[int]
    possibles: list[str]
    common_word: str
    decoded_text: str
    data: str = Path(__file__).parent.joinpath(filename).read_text(encoding="utf-8")

    ciphertext = [int(number) for number in data.strip().split(",")]

    possibles = filter_valid_chars(ciphertext)
    for common_word in COMMON_WORDS:
        possibles = filter_common_word(possibles, common_word)
        if len(possibles) == 1:
            break

    decoded_text = possibles[0]
    return sum(ord(char) for char in decoded_text)


if __name__ == "__main__":
    print(f"{solution() = }")
