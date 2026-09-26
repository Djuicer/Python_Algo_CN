"""
置换密码（Permutation Cipher）也称换位密码，是一种根据秘密密钥重新排列消息字符
的简单加密技术。它将消息分块，并按照密钥对每个块中的字符进行置换。密钥是一个
由互不相同的整数组成的序列，用于确定字符重排顺序。

更多信息：https://www.nku.edu/~christensen/1402%20permutation%20ciphers.pdf
"""

import random


def generate_valid_block_size(message_length: int) -> int:
    """
    生成一个作为消息长度因数的有效块大小。

    Args:
        message_length (int): The length of the message.

    Returns:
        int: A valid block size.

    Example:
        >>> random.seed(1)
        >>> generate_valid_block_size(12)
        3
    """
    block_sizes = [
        block_size
        for block_size in range(2, message_length + 1)
        if message_length % block_size == 0
    ]
    return random.choice(block_sizes)


def generate_permutation_key(block_size: int) -> list[int]:
    """
    生成指定块大小的随机置换密钥。

    Args:
        block_size (int): The size of each permutation block.

    Returns:
        list[int]: A list containing a random permutation of digits.

    Example:
        >>> random.seed(0)
        >>> generate_permutation_key(4)
        [2, 0, 1, 3]
    """
    digits = list(range(block_size))
    random.shuffle(digits)
    return digits


def encrypt(
    message: str, key: list[int] | None = None, block_size: int | None = None
) -> tuple[str, list[int]]:
    """
    使用密钥按块重排，以置换密码加密消息。

    Args:
        message (str): The plaintext message to be encrypted.
        key (list[int]): The permutation key for decryption.
        block_size (int): The size of each permutation block.

    Returns:
        tuple: A tuple containing the encrypted message and the encryption key.

    Example:
        >>> encrypted_message, key = encrypt("HELLO WORLD")
        >>> decrypted_message = decrypt(encrypted_message, key)
        >>> decrypted_message
        'HELLO WORLD'
    """
    message = message.upper()
    message_length = len(message)

    if key is None or block_size is None:
        block_size = generate_valid_block_size(message_length)
        key = generate_permutation_key(block_size)

    encrypted_message = ""

    for i in range(0, message_length, block_size):
        block = message[i : i + block_size]
        rearranged_block = [block[digit] for digit in key]
        encrypted_message += "".join(rearranged_block)

    return encrypted_message, key


def decrypt(encrypted_message: str, key: list[int]) -> str:
    """
    使用按块重排的置换密码解密消息。

    Args:
        encrypted_message (str): The encrypted message.
        key (list[int]): The permutation key for decryption.

    Returns:
        str: The decrypted plaintext message.

    Example:
        >>> encrypted_message, key = encrypt("HELLO WORLD")
        >>> decrypted_message = decrypt(encrypted_message, key)
        >>> decrypted_message
        'HELLO WORLD'
    """
    key_length = len(key)
    decrypted_message = ""

    for i in range(0, len(encrypted_message), key_length):
        block = encrypted_message[i : i + key_length]
        original_block = [""] * key_length
        for j, digit in enumerate(key):
            original_block[digit] = block[j]
        decrypted_message += "".join(original_block)

    return decrypted_message


def main() -> None:
    """
    驱动函数：传入消息，依次进行加密和解密。

    Example:
    >>> main()
    Decrypted message: HELLO WORLD
    """
    message = "HELLO WORLD"
    encrypted_message, key = encrypt(message)

    decrypted_message = decrypt(encrypted_message, key)
    print(f"Decrypted message: {decrypted_message}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    main()
