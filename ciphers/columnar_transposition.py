"""列换位密码（Columnar Transposition Cipher）。

这种古典密码将明文逐行写在关键字下方，再按照关键字中字母的字母序读取各列。

参考资料：https://en.wikipedia.org/wiki/Transposition_cipher#Columnar_transposition

保留空格和标点。key 必须仅含字母（不区分大小写）。

>>> pt = "WE ARE DISCOVERED. FLEE AT ONCE"
>>> ct = encrypt(pt, "ZEBRAS")
>>> decrypt(ct, "ZEBRAS") == pt
True

边界情况：
>>> encrypt("HELLO", "A")
'HELLO'
>>> decrypt("HELLO", "A")
'HELLO'
>>> encrypt("HELLO", "HELLO")
'EHLLO'
>>> decrypt("EHLLO", "HELLO")
'HELLO'
>>> encrypt("HELLO", "")
Traceback (most recent call last):
    ...
ValueError: Key must be a non-empty alphabetic string
"""

from __future__ import annotations


def _normalize_key(key: str) -> str:
    k = "".join(ch for ch in key.upper() if ch.isalpha())
    if not k:
        raise ValueError("Key must be a non-empty alphabetic string")
    return k


def _column_order(key: str) -> list[int]:
    # 先按字符、再按原始索引进行稳定排序，以处理重复字符
    indexed = list(enumerate(key))
    return [
        i
        for i, _ in sorted(
            indexed, key=lambda indexed_pair: (indexed_pair[1], indexed_pair[0])
        )
    ]


def encrypt(plaintext: str, key: str) -> str:
    """使用列换位密码加密。

    :param plaintext: 输入文本（可包含任意字符）
    :param key: 仅含字母的关键字
    :return: 密文
    :raises ValueError: key 无效时引发
    """
    k = _normalize_key(key)
    cols = len(k)
    if cols == 1:
        return plaintext

    order = _column_order(k)

    # 构造不使用填充的非等长行
    rows = (len(plaintext) + cols - 1) // cols
    grid: list[str] = [plaintext[i * cols : (i + 1) * cols] for i in range(rows)]

    # 按排序后的顺序读取各列，并跳过缺失单元格
    out: list[str] = []
    for col in order:
        for r in range(rows):
            if col < len(grid[r]):
                out.append(grid[r][col])
    return "".join(out)


def decrypt(ciphertext: str, key: str) -> str:
    """解密列换位密码的密文。

    :param ciphertext: 加密文本
    :param key: 仅含字母的关键字
    :return: 解密后的明文
    :raises ValueError: key 无效时引发
    """
    k = _normalize_key(key)
    cols = len(k)
    if cols == 1:
        return ciphertext

    order = _column_order(k)
    text_len = len(ciphertext)
    rows = (text_len + cols - 1) // cols
    r = text_len % cols

    # 根据非等长的最后一行确定列长（加密时未使用填充）
    col_lengths: list[int] = []
    for c in range(cols):
        if r == 0:
            col_lengths.append(rows)
        else:
            col_lengths.append(rows if c < r else rows - 1)

    # 按排序后的顺序将密文切分为各列
    columns: list[str] = [""] * cols
    idx = 0
    for col in order:
        ln = col_lengths[col]
        columns[col] = ciphertext[idx : idx + ln]
        idx += ln

    # 逐行重建明文
    out: list[str] = []
    pointers = [0] * cols
    for _ in range(rows * cols):
        c = len(out) % cols
        if pointers[c] < len(columns[c]):
            out.append(columns[c][pointers[c]])
            pointers[c] += 1
    return "".join(out)


if __name__ == "__main__":  # pragma: no cover
    import doctest

    doctest.testmod()
