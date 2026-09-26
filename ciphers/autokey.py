"""
https://en.wikipedia.org/wiki/Autokey_cipher

自动密钥密码（Autokey Cipher，也称 autoclave cipher）是一种将消息（明文）
纳入密钥的密码。密钥以某种自动方式从消息生成，有时从文本中选择特定字母，
更常见的方式是在消息前添加一个较短的初始密钥。
"""


def encrypt(plaintext: str, key: str) -> str:
    """
    使用给定的 `key`（字符串）加密 `plaintext`（字符串），返回加密后的密文。

    >>> encrypt("hello world", "coffee")
    'jsqqs avvwo'
    >>> encrypt("coffee is good as python", "TheAlgorithms")
    'vvjfpk wj ohvp su ddylsv'
    >>> encrypt("coffee is good as python", 2)
    Traceback (most recent call last):
        ...
    TypeError: key must be a string
    >>> encrypt("", "TheAlgorithms")
    Traceback (most recent call last):
        ...
    ValueError: plaintext is empty
    >>> encrypt("coffee is good as python", "")
    Traceback (most recent call last):
        ...
    ValueError: key is empty
    >>> encrypt(527.26, "TheAlgorithms")
    Traceback (most recent call last):
        ...
    TypeError: plaintext must be a string
    """
    if not isinstance(plaintext, str):
        raise TypeError("plaintext must be a string")
    if not isinstance(key, str):
        raise TypeError("key must be a string")

    if not plaintext:
        raise ValueError("plaintext is empty")
    if not key:
        raise ValueError("key is empty")

    key += plaintext
    plaintext = plaintext.lower()
    key = key.lower()
    plaintext_iterator = 0
    key_iterator = 0
    ciphertext = ""
    while plaintext_iterator < len(plaintext):
        if (
            ord(plaintext[plaintext_iterator]) < 97
            or ord(plaintext[plaintext_iterator]) > 122
        ):
            ciphertext += plaintext[plaintext_iterator]
            plaintext_iterator += 1
        elif ord(key[key_iterator]) < 97 or ord(key[key_iterator]) > 122:
            key_iterator += 1
        else:
            ciphertext += chr(
                (
                    (ord(plaintext[plaintext_iterator]) - 97 + ord(key[key_iterator]))
                    - 97
                )
                % 26
                + 97
            )
            key_iterator += 1
            plaintext_iterator += 1
    return ciphertext


def decrypt(ciphertext: str, key: str) -> str:
    """
    使用给定的 `key`（字符串）解密 `ciphertext`（字符串），返回解密后的文本。

    >>> decrypt("jsqqs avvwo", "coffee")
    'hello world'
    >>> decrypt("vvjfpk wj ohvp su ddylsv", "TheAlgorithms")
    'coffee is good as python'
    >>> decrypt("vvjfpk wj ohvp su ddylsv", "")
    Traceback (most recent call last):
        ...
    ValueError: key is empty
    >>> decrypt(527.26, "TheAlgorithms")
    Traceback (most recent call last):
        ...
    TypeError: ciphertext must be a string
    >>> decrypt("", "TheAlgorithms")
    Traceback (most recent call last):
        ...
    ValueError: ciphertext is empty
    >>> decrypt("vvjfpk wj ohvp su ddylsv", 2)
    Traceback (most recent call last):
        ...
    TypeError: key must be a string
    """
    if not isinstance(ciphertext, str):
        raise TypeError("ciphertext must be a string")
    if not isinstance(key, str):
        raise TypeError("key must be a string")

    if not ciphertext:
        raise ValueError("ciphertext is empty")
    if not key:
        raise ValueError("key is empty")

    key = key.lower()
    ciphertext_iterator = 0
    key_iterator = 0
    plaintext = ""
    while ciphertext_iterator < len(ciphertext):
        if (
            ord(ciphertext[ciphertext_iterator]) < 97
            or ord(ciphertext[ciphertext_iterator]) > 122
        ):
            plaintext += ciphertext[ciphertext_iterator]
        else:
            plaintext += chr(
                (ord(ciphertext[ciphertext_iterator]) - ord(key[key_iterator])) % 26
                + 97
            )
            key += chr(
                (ord(ciphertext[ciphertext_iterator]) - ord(key[key_iterator])) % 26
                + 97
            )
            key_iterator += 1
        ciphertext_iterator += 1
    return plaintext


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    operation = int(input("Type 1 to encrypt or 2 to decrypt:"))
    if operation == 1:
        plaintext = input("Typeplaintext to be encrypted:\n")
        key = input("Type the key:\n")
        print(encrypt(plaintext, key))
    elif operation == 2:
        ciphertext = input("Type the ciphertext to be decrypted:\n")
        key = input("Type the key:\n")
        print(decrypt(ciphertext, key))
    decrypt("jsqqs avvwo", "coffee")
