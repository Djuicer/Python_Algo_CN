#!/usr/bin/env python3

"""
波利比奥斯方阵（Polybius Square）是一种将字母转换为数字的表格。

https://www.braingle.com/brainteasers/codes/polybius.php
"""

import numpy as np

SQUARE = [
    ["a", "b", "c", "d", "e"],
    ["f", "g", "h", "i", "k"],
    ["l", "m", "n", "o", "p"],
    ["q", "r", "s", "t", "u"],
    ["v", "w", "x", "y", "z"],
]


class PolybiusCipher:
    def __init__(self) -> None:
        self.SQUARE = np.array(SQUARE)

    def letter_to_numbers(self, letter: str) -> np.ndarray:
        """
        返回给定字母在波利比奥斯方阵中对应的数字对。
        >>> np.array_equal(PolybiusCipher().letter_to_numbers('a'), [1,1])
        True

        >>> np.array_equal(PolybiusCipher().letter_to_numbers('u'), [4,5])
        True
        """
        index1, index2 = np.where(letter == self.SQUARE)
        indexes = np.concatenate([index1 + 1, index2 + 1])
        return indexes

    def numbers_to_letter(self, index1: int, index2: int) -> str:
        """
        返回波利比奥斯方阵中位置 [index1, index2] 对应的字母。

        >>> PolybiusCipher().numbers_to_letter(4, 5) == "u"
        True

        >>> PolybiusCipher().numbers_to_letter(1, 1) == "a"
        True
        """
        return self.SQUARE[index1 - 1, index2 - 1]

    def encode(self, message: str) -> str:
        """
        返回按照波利比奥斯密码编码后的 message。

        >>> PolybiusCipher().encode("test message") == "44154344 32154343112215"
        True

        >>> PolybiusCipher().encode("Test Message") == "44154344 32154343112215"
        True
        """
        message = message.lower()
        message = message.replace("j", "i")

        encoded_message = ""
        for letter_index in range(len(message)):
            if message[letter_index] != " ":
                numbers = self.letter_to_numbers(message[letter_index])
                encoded_message = encoded_message + str(numbers[0]) + str(numbers[1])
            elif message[letter_index] == " ":
                encoded_message = encoded_message + " "

        return encoded_message

    def decode(self, message: str) -> str:
        """
        返回按照波利比奥斯密码解码后的 message。

        >>> PolybiusCipher().decode("44154344 32154343112215") == "test message"
        True

        >>> PolybiusCipher().decode("4415434432154343112215") == "testmessage"
        True
        """
        message = message.replace(" ", "  ")
        decoded_message = ""
        for numbers_index in range(int(len(message) / 2)):
            if message[numbers_index * 2] != " ":
                index1 = message[numbers_index * 2]
                index2 = message[numbers_index * 2 + 1]

                letter = self.numbers_to_letter(int(index1), int(index2))
                decoded_message = decoded_message + letter
            elif message[numbers_index * 2] == " ":
                decoded_message = decoded_message + " "

        return decoded_message
