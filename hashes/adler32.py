"""
Adler-32 是 Mark Adler 于 1995 年发明的一种校验和算法。
与相同长度的循环冗余校验相比，它以可靠性换取速度（更侧重后者）。
Adler-32 比 Fletcher-16 更可靠，但可靠性略低于 Fletcher-32。[2]

来源：https://en.wikipedia.org/wiki/Adler-32
"""

MOD_ADLER = 65521


def adler32(plain_text: str) -> int:
    """
    实现 Adler-32 哈希。
    遍历每个字符并计算新值。

    >>> adler32('Algorithms')
    363791387

    >>> adler32('go adler em all')
    708642122
    """
    a = 1
    b = 0
    for plain_chr in plain_text:
        a = (a + ord(plain_chr)) % MOD_ADLER
        b = (b + a) % MOD_ADLER
    return (b << 16) | a
