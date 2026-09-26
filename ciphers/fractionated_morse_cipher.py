"""
分式摩尔斯密码（Fractionated Morse Cipher）的 Python 程序。

分式摩尔斯密码先将明文转换为摩尔斯电码，再把固定大小的摩尔斯电码块加密回字母。
这一过程会将明文字母混合到密文字母中，使其比替换密码更安全。

http://practicalcryptography.com/ciphers/fractionated-morse-cipher/
"""

import string

MORSE_CODE_DICT = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    " ": "",
}

# Define possible trigrams of Morse code
MORSE_COMBINATIONS = [
    "...",
    "..-",
    "..x",
    ".-.",
    ".--",
    ".-x",
    ".x.",
    ".x-",
    ".xx",
    "-..",
    "-.-",
    "-.x",
    "--.",
    "---",
    "--x",
    "-x.",
    "-x-",
    "-xx",
    "x..",
    "x.-",
    "x.x",
    "x-.",
    "x--",
    "x-x",
    "xx.",
    "xx-",
    "xxx",
]

# Create a reverse dictionary for Morse code
REVERSE_DICT = {value: key for key, value in MORSE_CODE_DICT.items()}


def encode_to_morse(plaintext: str) -> str:
    """将明文消息编码为摩尔斯电码。

    Args:
        plaintext: The plaintext message to encode.

    返回值：
        明文消息的摩尔斯电码表示。

    示例：
        >>> encode_to_morse("defend the east")
        '-..x.x..-.x.x-.x-..xx-x....x.xx.x.-x...x-'
    """
    return "x".join([MORSE_CODE_DICT.get(letter.upper(), "") for letter in plaintext])


def encrypt_fractionated_morse(plaintext: str, key: str) -> str:
    """使用分式摩尔斯密码加密明文消息。

    Args:
        plaintext: The plaintext message to encrypt.
        key: The encryption key.

    返回值：
        加密后的密文。

    示例：
        >>> encrypt_fractionated_morse("defend the east","Roundtable")
        'ESOAVVLJRSSTRX'

    """
    morse_code = encode_to_morse(plaintext)
    key = key.upper() + string.ascii_uppercase
    key = "".join(sorted(set(key), key=key.find))

    # Ensure morse_code length is a multiple of 3
    padding_length = 3 - (len(morse_code) % 3)
    morse_code += "x" * padding_length

    fractionated_morse_dict = {v: k for k, v in zip(key, MORSE_COMBINATIONS)}
    fractionated_morse_dict["xxx"] = ""
    encrypted_text = "".join(
        [
            fractionated_morse_dict[morse_code[i : i + 3]]
            for i in range(0, len(morse_code), 3)
        ]
    )
    return encrypted_text


def decrypt_fractionated_morse(ciphertext: str, key: str) -> str:
    """解密由分式摩尔斯密码加密的密文消息。

    Args:
        ciphertext: The ciphertext message to decrypt.
        key: The decryption key.

    返回值：
        解密后的明文消息。

    示例：
        >>> decrypt_fractionated_morse("ESOAVVLJRSSTRX","Roundtable")
        'DEFEND THE EAST'
    """
    key = key.upper() + string.ascii_uppercase
    key = "".join(sorted(set(key), key=key.find))

    inverse_fractionated_morse_dict = dict(zip(key, MORSE_COMBINATIONS))
    morse_code = "".join(
        [inverse_fractionated_morse_dict.get(letter, "") for letter in ciphertext]
    )
    decrypted_text = "".join(
        [REVERSE_DICT[code] for code in morse_code.split("x")]
    ).strip()
    return decrypted_text


if __name__ == "__main__":
    """
    分式摩尔斯密码的用法示例。
    """
    plaintext = "defend the east"
    print("Plain Text:", plaintext)
    key = "ROUNDTABLE"

    ciphertext = encrypt_fractionated_morse(plaintext, key)
    print("Encrypted:", ciphertext)

    decrypted_text = decrypt_fractionated_morse(ciphertext, key)
    print("Decrypted:", decrypted_text)
