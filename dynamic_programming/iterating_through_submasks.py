"""
Author : Syed Faizan (3rd Year Student IIIT Pune)
github : faizan2700
给定一个位掩码 m，需要高效遍历它的所有子掩码。
如果掩码 s 中置位的位都包含在位掩码 m 中，则 s 是 m 的子掩码。
"""

from __future__ import annotations


def list_of_submasks(mask: int) -> list[int]:
    """
    参数：
        mask : 表示掩码的数（始终为 integer > 0，零没有任何子掩码）

    返回：
        all_submasks : mask 的子掩码列表（如果掩码 s 中置位的位都包含在原始掩码
        m 中，则称掩码 s 为掩码 m 的子掩码）

    异常：
        AssertionError: mask 不是正整数

    >>> list_of_submasks(15)
    [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    >>> list_of_submasks(13)
    [13, 12, 9, 8, 5, 4, 1]
    >>> list_of_submasks(-7)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    AssertionError: mask needs to be positive integer, your input -7
    >>> list_of_submasks(0)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    AssertionError: mask needs to be positive integer, your input 0

    """

    assert isinstance(mask, int) and mask > 0, (
        f"mask needs to be positive integer, your input {mask}"
    )

    """
    遍历的第一个子掩码是 mask 本身，随后执行运算以获得其他子掩码，
    直到到达值为零的空子掩码（最终的子掩码列表不包含零）
    """
    all_submasks = []
    submask = mask

    while submask:
        all_submasks.append(submask)
        submask = (submask - 1) & mask

    return all_submasks


if __name__ == "__main__":
    import doctest

    doctest.testmod()
