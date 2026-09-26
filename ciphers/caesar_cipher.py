from __future__ import annotations

from string import ascii_letters


def encrypt(input_string: str, key: int, alphabet: str | None = None) -> str:
    """
    加密
    =======

    使用凯撒密码（Caesar Cipher）编码给定字符串，并返回编码后的消息。

    参数：
    -----------

    *   `input_string`: 需要编码的明文
    *   `key`: 消息要移位的字母数量

    可选参数：

    *   `alphabet` (``None``): 编码密码时使用的字母表；未指定时使用包含大小写字母的
        标准英文字母表

    返回值：

    *   包含编码后密文的字符串

    关于凯撒密码
    =========================

    凯撒密码以 Julius Caesar 命名，他曾用这种密码向军队发送秘密军事消息。这是
    一种简单替换密码，明文中的每个字符都移动一定数量的位置，该数量称为“密钥”
    或“移位量”。

    示例：
    假设有以下消息：
    ``Hello, captain``

    字母表由大小写字母组成：
    ``abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ``

    移位量为 ``2``

    随后可逐字母编码消息。``H`` 会变为 ``J``，因为 ``J`` 与其相隔两个位置，
    其余字母以此类推。如果移位超出字母表末尾，则从开头继续（``Z`` 会依次
    移位到 ``a``、``b`` 等）。

    最终消息为 ``Jgnnq, ecrvckp``

    延伸阅读
    ===============

    *   https://en.m.wikipedia.org/wiki/Caesar_cipher

    Doctest
    ========

    >>> encrypt('The quick brown fox jumps over the lazy dog', 8)
    'bpm yCqks jzwEv nwF rCuxA wDmz Bpm tiHG lwo'

    >>> encrypt('A very large key', 8000)
    's nWjq dSjYW cWq'

    >>> encrypt('a lowercase alphabet', 5, 'abcdefghijklmnopqrstuvwxyz')
    'f qtbjwhfxj fqumfgjy'
    """
    # 将默认字母表设为大小写英文字母
    alpha = alphabet or ascii_letters

    # 最终结果字符串
    result = ""

    for character in input_string:
        if character not in alpha:
            # 如果字符不在字母表中，则不加密，直接追加
            result += character
        else:
            # 获取新密钥的索引，并确保其不超出范围
            new_key = (alpha.index(character) + key) % len(alpha)

            # 追加编码后的字符
            result += alpha[new_key]

    return result


def decrypt(input_string: str, key: int, alphabet: str | None = None) -> str:
    """
    解密
    =======

    解码给定密文字符串，并返回解码后的明文。

    参数：
    -----------

    *   `input_string`: 需要解码的密文
    *   `key`: 解码时消息向后移位的字母数量

    可选参数：

    *   `alphabet` (``None``): 解码密码时使用的字母表；未指定时使用包含大小写字母的
        标准英文字母表

    返回值：

    *   包含解码后明文的字符串

    关于凯撒密码
    =========================

    凯撒密码以 Julius Caesar 命名，他曾用这种密码向军队发送秘密军事消息。这是
    一种简单替换密码，明文中的每个字符都移动一定数量的位置，该数量称为“密钥”
    或“移位量”。此处重点介绍解密。

    示例：
    假设有以下密文：
    ``Jgnnq, ecrvckp``

    字母表由大小写字母组成：
    ``abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ``

    移位量为 ``2``

    解码执行与编码相反的操作。首字母 ``J`` 会变为 ``H``，因为 ``H`` 位于 ``J``
    向后（向左）两个位置。其余字母继续如此处理；``a`` 等字母向后移动时会绕到
    字母表末尾，变为 ``Z``、``Y`` 等。

    最终消息为 ``Hello, captain``

    延伸阅读
    ===============

    *   https://en.m.wikipedia.org/wiki/Caesar_cipher

    Doctest
    ========

    >>> decrypt('bpm yCqks jzwEv nwF rCuxA wDmz Bpm tiHG lwo', 8)
    'The quick brown fox jumps over the lazy dog'

    >>> decrypt('s nWjq dSjYW cWq', 8000)
    'A very large key'

    >>> decrypt('f qtbjwhfxj fqumfgjy', 5, 'abcdefghijklmnopqrstuvwxyz')
    'a lowercase alphabet'
    """
    # 将密钥取负以启用解码模式
    key *= -1

    return encrypt(input_string, key, alphabet)


def brute_force(input_string: str, alphabet: str | None = None) -> dict[int, str]:
    """
    暴力破解
    ===========

    以字典形式返回所有可能的密钥组合及其对应的解码字符串。

    参数：
    -----------

    *   `input_string`: 暴力破解时使用的密文

    可选参数：

    *   `alphabet` (``None``): 解码密码时使用的字母表；未指定时使用包含大小写字母的
        标准英文字母表

    关于暴力破解
    ======================

    暴力破解是指截获消息或密码后，在不知道密钥的情况下尝试所有组合。凯撒密码
    只有字母表范围内的有限种组合，因此较易暴力破解；密码越复杂，暴力破解所需
    时间越长。

    示例：
    为简化说明，假设字母表包含 ``5`` 个字母（``abcde``），截获消息 ``dbc``。
    可以依次写出每种组合：``ecd``……直到得到有意义的组合：
    ``cab``

    延伸阅读
    ===============

    *   https://en.wikipedia.org/wiki/Brute_force

    Doctest
    ========

    >>> brute_force("jFyuMy xIH'N vLONy zILwy Gy!")[20]
    "Please don't brute force me!"

    >>> brute_force(1)
    Traceback (most recent call last):
    TypeError: 'int' object is not iterable
    """
    # 将默认字母表设为大小写英文字母
    alpha = alphabet or ascii_letters

    # 存储所有组合的数据
    brute_force_data = {}

    # 遍历每种组合
    for key in range(1, len(alpha) + 1):
        # 解密消息并保存结果
        brute_force_data[key] = decrypt(input_string, key, alpha)

    return brute_force_data


if __name__ == "__main__":
    while True:
        print(f"\n{'-' * 10}\n Menu\n{'-' * 10}")
        print(*["1.Encrypt", "2.Decrypt", "3.BruteForce", "4.Quit"], sep="\n")

        # 获取用户输入
        choice = input("\nWhat would you like to do?: ").strip() or "4"

        # 根据用户选择运行相应函数
        if choice not in ("1", "2", "3", "4"):
            print("Invalid choice, please enter a valid choice")
        elif choice == "1":
            input_string = input("Please enter the string to be encrypted: ")
            key = int(input("Please enter off-set: ").strip())

            print(encrypt(input_string, key))
        elif choice == "2":
            input_string = input("Please enter the string to be decrypted: ")
            key = int(input("Please enter off-set: ").strip())

            print(decrypt(input_string, key))
        elif choice == "3":
            input_string = input("Please enter the string to be decrypted: ")
            brute_force_data = brute_force(input_string)

            for key, value in brute_force_data.items():
                print(f"Key: {key} | Message: {value}")

        elif choice == "4":
            print("Goodbye.")
            break
