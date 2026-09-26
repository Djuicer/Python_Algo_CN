"""
RC4（Rivest Cipher 4）流密码算法
=============================================

RC4 是 Ron Rivest 于 1987 年为 RSA Security 设计的对称流密码，以实现简单且软件
运行速度快而著称。它按字节运行，通过将明文与伪随机密钥流进行 XOR，逐字节加密
和解密数据。

工作原理：
-------------
1. Key Scheduling Algorithm (KSA):
   Initializes and permutes a 256-byte state array (the S-box) based on the secret key.
2. Pseudo-Random Generation Algorithm (PRGA):
   Generates a continuous sequence of pseudorandom bytes (the keystream)
   from the S-box.
   With each byte generated, the state array is mutated to ensure unpredictability.
3. Encryption/Decryption:
   The plaintext is XORed byte-by-byte with the keystream to produce the ciphertext.
   Since XOR is its own inverse, decryption uses the exact same process (XORing
   the ciphertext with the same keystream).

Security Status:
----------------
WARNING: RC4 is cryptographically broken and insecure.
It suffers from significant keystream biases, particularly in the initial bytes.
If the same key is reused, or if an attacker captures enough ciphertext, they
can reconstruct the plaintext or the key. The use of RC4 is prohibited in modern
protocols (such as TLS via RFC 7465). It is implemented here strictly for
educational purposes.

Further reading:
----------------
* https://en.wikipedia.org/wiki/RC4
"""

from collections.abc import Generator


def ksa(key: bytes) -> list[int]:
    """
    密钥调度算法（KSA）
    ==============================

    KSA 使用 0 到 255 初始化大小为 256 的数组 S（S-box）中的置换，再使用秘密
    密钥打乱该数组。

    参数：
    -----------
    * `key`: 用于加密/解密的秘密密钥，类型为 bytes。

    返回值：
    --------
    * A list of 256 integers representing the permuted S-box.

    Doctests:
    =========
    >>> ksa(b"Key")[:5]
    [75, 51, 132, 157, 192]
    """
    s_box = list(range(256))
    j = 0
    key_length = len(key)
    for i in range(256):
        j = (j + s_box[i] + key[i % key_length]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]
    return s_box


def prga(s_box: list[int]) -> Generator[int]:
    """
    伪随机生成算法（PRGA）
    =========================================

    PRGA 从置换后的 S-box S 生成密钥流字节。每次迭代都会修改 S-box，并输出一个
    密钥流字节。

    Parameters:
    -----------
    * `s_box`: The permuted state array S-box.

    Yields:
    -------
    * An integer representing the next byte of the pseudo-random keystream.

    Doctests:
    =========
    >>> box = ksa(b"Key")
    >>> stream = prga(box)
    >>> [next(stream) for _ in range(5)]
    [235, 159, 119, 129, 183]
    """
    s = s_box.copy()
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        yield s[(s[i] + s[j]) % 256]


def encrypt(plaintext: bytes, key: bytes) -> bytes:
    """
    使用 RC4 流密码和密钥加密/解密明文字节。

    Parameters:
    -----------
    * `plaintext`: The input message to encrypt/decrypt (bytes).
    * `key`: The secret key (bytes).

    Returns:
    --------
    * The encrypted/decrypted result (bytes).

    More on RC4:
    ============
    RC4 (Rivest Cipher 4) is a symmetric stream cipher. Because it is symmetric,
    the encryption and decryption operations are identical. The cipher
    generates a pseudorandom stream of bytes (keystream) which is combined with
    the plaintext using bitwise exclusive-or (XOR).

    Warning:
    --------
    RC4 is cryptographically insecure and vulnerable to several attacks (such
    as keystream biases). It should not be used in secure systems today. It is
    implemented here purely for educational purposes.

    Further reading:
    ================
    * https://en.wikipedia.org/wiki/RC4

    Doctests:
    =========
    >>> encrypt(b"Plaintext", b"Key")
    b'\\xbb\\xf3\\x16\\xe8\\xd9@\\xaf\\n\\xd3'
    >>> encrypt(b"pedia", b"Wiki")
    b'\\x10!\\xbf\\x04 '
    >>> encrypt(b"\\x10!\\xbf\\x04 ", b"Wiki")
    b'pedia'
    """
    if not key:
        raise ValueError("Key must not be empty.")

    s_box = ksa(key)
    keystream = prga(s_box)
    return bytes(p ^ next(keystream) for p in plaintext)


def decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """
    使用 RC4 流密码和密钥解密密文字节。

    RC4 是对称密码，因此解密过程与加密过程相同。

    Parameters:
    -----------
    * `ciphertext`: The input cipher text to decrypt (bytes).
    * `key`: The secret key (bytes).

    Returns:
    --------
    * The decrypted plaintext (bytes).

    Doctests:
    =========
    >>> decrypt(b'\\x10!\\xbf\\x04 ', b"Wiki")
    b'pedia'
    """
    return encrypt(ciphertext, key)


if __name__ == "__main__":
    import sys

    # Check for doctests
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        import doctest

        doctest.testmod()
        sys.exit(0)

    print(f"\n{'-' * 10}\n RC4 Cipher Menu\n{'-' * 10}")
    print("1. Encrypt String")
    print("2. Decrypt Hex String")
    print("3. Quit")

    while True:
        choice = input("\nWhat would you like to do?: ").strip()
        if choice == "3" or not choice:
            print("Goodbye.")
            break
        elif choice == "1":
            plain_str = input("Enter plain text to encrypt: ")
            key_str = input("Enter key: ")
            if not key_str:
                print("Key cannot be empty!")
                continue
            encrypted_bytes = encrypt(
                plain_str.encode("utf-8"), key_str.encode("utf-8")
            )
            print(f"Ciphertext (Hex): {encrypted_bytes.hex()}")
        elif choice == "2":
            hex_str = input("Enter hex ciphertext to decrypt: ")
            key_str = input("Enter key: ")
            if not key_str:
                print("Key cannot be empty!")
                continue
            try:
                cipher_bytes = bytes.fromhex(hex_str)
                decrypted_bytes = decrypt(cipher_bytes, key_str.encode("utf-8"))
                decrypted_text = decrypted_bytes.decode("utf-8", errors="replace")
                print(f"Decrypted text: {decrypted_text}")
            except ValueError as e:
                print(f"Invalid input: {e}")
        else:
            print("Invalid choice, please enter 1, 2, or 3.")
