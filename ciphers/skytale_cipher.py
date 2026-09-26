"""密码棒（Scytale/Skytale）换位密码。

这是古希腊使用的一种古典换位密码。发送者将羊皮纸条缠绕在密码棒上，沿棒书写
消息；接收者使用直径相同的棒即可读取消息。

参考资料：https://en.wikipedia.org/wiki/Scytale

这里的函数保持字符原样（包括空格）。key 是表示周长计数（行数）的正整数。

>>> encrypt("WE ARE DISCOVERED FLEE AT ONCE", 3)
'WA SVEFETNERDCEDL  C EIOR EAOE'
>>> decrypt('WA SVEFETNERDCEDL  C EIOR EAOE', 3)
'WE ARE DISCOVERED FLEE AT ONCE'

Edge cases:
>>> encrypt("HELLO", 1)
'HELLO'
>>> decrypt("HELLO", 1)
'HELLO'
>>> encrypt("HELLO", 5)  # key equals length
'HELLO'
>>> decrypt("HELLO", 5)
'HELLO'
>>> encrypt("HELLO", 0)
Traceback (most recent call last):
    ...
ValueError: Key must be a positive integer
>>> decrypt("HELLO", -2)
Traceback (most recent call last):
    ...
ValueError: Key must be a positive integer
"""

from __future__ import annotations


def encrypt(plaintext: str, key: int) -> str:
    """使用密码棒换位法加密明文。

    将字符写在具有 `key` 行的棒上，再逐行读出。

    :param plaintext: Input message to encrypt
    :param key: Positive integer number of rows
    :return: Ciphertext string
    :raises ValueError: if key <= 0
    """
    if key <= 0:
        raise ValueError("Key must be a positive integer")
    if key == 1 or len(plaintext) <= key:
        return plaintext

    # Read every key-th character starting from each row offset
    return "".join(plaintext[row::key] for row in range(key))


def decrypt(ciphertext: str, key: int) -> str:
    """解密密码棒密文。

    按各行长度重建行，再逐列交错组合。

    :param ciphertext: Encrypted string
    :param key: Positive integer number of rows
    :return: Decrypted plaintext
    :raises ValueError: if key <= 0
    """
    if key <= 0:
        raise ValueError("Key must be a positive integer")
    if key == 1 or len(ciphertext) <= key:
        return ciphertext

    length = len(ciphertext)
    base = length // key
    extra = length % key

    # Determine each row length
    row_lengths: list[int] = [base + (1 if r < extra else 0) for r in range(key)]

    # Slice ciphertext into rows
    rows: list[str] = []
    idx = 0
    for r_len in row_lengths:
        rows.append(ciphertext[idx : idx + r_len])
        idx += r_len

    # Pointers to current index in each row
    pointers = [0] * key

    # Reconstruct by taking characters column-wise across rows
    result_chars: list[str] = []
    for i in range(length):
        r = i % key
        if pointers[r] < len(rows[r]):
            result_chars.append(rows[r][pointers[r]])
            pointers[r] += 1
    return "".join(result_chars)


if __name__ == "__main__":  # pragma: no cover
    import doctest

    doctest.testmod()
