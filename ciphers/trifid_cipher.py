"""
Trifid 密码使用表格将每个明文字母分解为三元组，混合三元组的组成部分，再反向
应用该表，将混合后的三元组转换为密文字母。

https://en.wikipedia.org/wiki/Trifid_cipher
"""

from __future__ import annotations

# fmt: off
TEST_CHARACTER_TO_NUMBER = {
    "A": "111", "B": "112", "C": "113", "D": "121", "E": "122", "F": "123", "G": "131",
    "H": "132", "I": "133", "J": "211", "K": "212", "L": "213", "M": "221", "N": "222",
    "O": "223", "P": "231", "Q": "232", "R": "233", "S": "311", "T": "312", "U": "313",
    "V": "321", "W": "322", "X": "323", "Y": "331", "Z": "332", "+": "333",
}
# fmt: off

TEST_NUMBER_TO_CHARACTER = {val: key for key, val in TEST_CHARACTER_TO_NUMBER.items()}


def __encrypt_part(message_part: str, character_to_number: dict[str, str]) -> str:
    """
    纵向排列 `message_part` 中每个字母的三元组值，再横向拼接。

    >>> __encrypt_part('ASK', TEST_CHARACTER_TO_NUMBER)
    '132111112'
    """
    one, two, three = "", "", ""
    for each in (character_to_number[character] for character in message_part):
        one += each[0]
        two += each[1]
        three += each[2]

    return one + two + three


def __decrypt_part(
    message_part: str, character_to_number: dict[str, str]
) -> tuple[str, str, str]:
    """
    将输入字符串中的每个字母转换为对应三元组值，拼接后分成三个等长字符串并返回。

    >>> __decrypt_part('ABCDE', TEST_CHARACTER_TO_NUMBER)
    ('11111', '21131', '21122')
    """
    this_part = "".join(character_to_number[character] for character in message_part)
    result = []
    tmp = ""
    for digit in this_part:
        tmp += digit
        if len(tmp) == len(message_part):
            result.append(tmp)
            tmp = ""

    return result[0], result[1], result[2]


def __prepare(
    message: str, alphabet: str
) -> tuple[str, str, dict[str, str], dict[str, str]]:
    """
    辅助函数：确认字母表长度为 ``27`` 后生成三元组，将字母表中的每个字母分配给
    对应三元组，并存入字典（`character_to_number` 和 `number_to_character`）。

    >>> test = __prepare('I aM a BOy','abCdeFghijkLmnopqrStuVwxYZ+')
    >>> expected = ('IAMABOY','ABCDEFGHIJKLMNOPQRSTUVWXYZ+',
    ... TEST_CHARACTER_TO_NUMBER, TEST_NUMBER_TO_CHARACTER)
    >>> test == expected
    True

    Testing with incomplete alphabet

    >>> __prepare('I aM a BOy','abCdeFghijkLmnopqrStuVw')
    Traceback (most recent call last):
        ...
    KeyError: 'Length of alphabet has to be 27.'

    Testing with extra long alphabets

    >>> __prepare('I aM a BOy','abCdeFghijkLmnopqrStuVwxyzzwwtyyujjgfd')
    Traceback (most recent call last):
        ...
    KeyError: 'Length of alphabet has to be 27.'

    Testing with punctuation not in the given alphabet

    >>> __prepare('am i a boy?','abCdeFghijkLmnopqrStuVwxYZ+')
    Traceback (most recent call last):
        ...
    ValueError: Each message character has to be included in alphabet!

    Testing with numbers

    >>> __prepare(500,'abCdeFghijkLmnopqrStuVwxYZ+')
    Traceback (most recent call last):
        ...
    AttributeError: 'int' object has no attribute 'replace'
    """
    # Validate message and alphabet, set to upper and remove spaces
    alphabet = alphabet.replace(" ", "").upper()
    message = message.replace(" ", "").upper()

    # Check length and characters
    if len(alphabet) != 27:
        raise KeyError("Length of alphabet has to be 27.")
    if any(char not in alphabet for char in message):
        raise ValueError("Each message character has to be included in alphabet!")

    # Generate dictionares
    character_to_number = dict(zip(alphabet, TEST_CHARACTER_TO_NUMBER.values()))
    number_to_character = {
        number: letter for letter, number in character_to_number.items()
    }

    return message, alphabet, character_to_number, number_to_character


def encrypt_message(
    message: str, alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ.", period: int = 5
) -> str:
    """
    encrypt_message
    ===============

    使用 trifid_cipher 加密消息。所有要使用的标点字符都应加入字母表。

    PARAMETERS
    ----------

    *   `message`: The message you want to encrypt.
    *   `alphabet` (optional): The characters to be used for the cipher .
    *   `period` (optional): The number of characters you want in a group whilst
        encrypting.

    >>> encrypt_message('I am a boy')
    'BCDGBQY'

    >>> encrypt_message(' ')
    ''

    >>> encrypt_message('   aide toi le c  iel      ta id  era    ',
    ... 'FELIXMARDSTBCGHJKNOPQUVWYZ+',5)
    'FMJFVOISSUFTFPUFEQQC'

    """
    message, alphabet, character_to_number, number_to_character = __prepare(
        message, alphabet
    )

    encrypted_numeric = ""
    for i in range(0, len(message) + 1, period):
        encrypted_numeric += __encrypt_part(
            message[i : i + period], character_to_number
        )

    encrypted = ""
    for i in range(0, len(encrypted_numeric), 3):
        encrypted += number_to_character[encrypted_numeric[i : i + 3]]
    return encrypted


def decrypt_message(
    message: str, alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ.", period: int = 5
) -> str:
    """
    decrypt_message
    ===============

    解密由 trifid_cipher 加密的消息。

    PARAMETERS
    ----------

    *   `message`: The message you want to decrypt.
    *   `alphabet` (optional): The characters used for the cipher.
    *   `period` (optional): The number of characters used in grouping when it
        was encrypted.

    >>> decrypt_message('BCDGBQY')
    'IAMABOY'

    Decrypting with your own alphabet and period

    >>> decrypt_message('FMJFVOISSUFTFPUFEQQC','FELIXMARDSTBCGHJKNOPQUVWYZ+',5)
    'AIDETOILECIELTAIDERA'
    """
    message, alphabet, character_to_number, number_to_character = __prepare(
        message, alphabet
    )

    decrypted_numeric = []
    for i in range(0, len(message), period):
        a, b, c = __decrypt_part(message[i : i + period], character_to_number)

        for j in range(len(a)):
            decrypted_numeric.append(a[j] + b[j] + c[j])

    return "".join(number_to_character[each] for each in decrypted_numeric)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    msg = "DEFEND THE EAST WALL OF THE CASTLE."
    encrypted = encrypt_message(msg, "EPSDUCVWYM.ZLKXNBTFGORIJHAQ")
    decrypted = decrypt_message(encrypted, "EPSDUCVWYM.ZLKXNBTFGORIJHAQ")
    print(f"Encrypted: {encrypted}\nDecrypted: {decrypted}")
