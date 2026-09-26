"""
https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform

Burrows-Wheeler 变换（BWT，也称块排序压缩）将字符串重新排列，使相似字符
连续出现。这有利于压缩，因为包含连续重复字符的字符串通常容易使用前移变换、
游程编码等技术压缩。更重要的是，该变换可逆，除原字符串首字符的位置外，
无需存储任何额外数据。因此，BWT 只增加一些计算量，便能“免费”提高文本压缩
算法的效率。
"""

from __future__ import annotations

from typing import TypedDict


class BWTTransformDict(TypedDict):
    bwt_string: str
    idx_original_string: int


def all_rotations(s: str) -> list[str]:
    """
    :param s: 将循环移位 len(s) 次的字符串。
    :return: 包含各次循环移位结果的列表。
    :raises TypeError: s 不是 str 实例时引发。
    示例：

    >>> all_rotations("^BANANA|") # doctest: +NORMALIZE_WHITESPACE
    ['^BANANA|', 'BANANA|^', 'ANANA|^B', 'NANA|^BA', 'ANA|^BAN', 'NA|^BANA',
    'A|^BANAN', '|^BANANA']
    >>> all_rotations("a_asa_da_casa") # doctest: +NORMALIZE_WHITESPACE
    ['a_asa_da_casa', '_asa_da_casaa', 'asa_da_casaa_', 'sa_da_casaa_a',
    'a_da_casaa_as', '_da_casaa_asa', 'da_casaa_asa_', 'a_casaa_asa_d',
    '_casaa_asa_da', 'casaa_asa_da_', 'asaa_asa_da_c', 'saa_asa_da_ca',
    'aa_asa_da_cas']
    >>> all_rotations("panamabanana") # doctest: +NORMALIZE_WHITESPACE
    ['panamabanana', 'anamabananap', 'namabananapa', 'amabananapan',
    'mabananapana', 'abananapanam', 'bananapanama', 'ananapanamab',
    'nanapanamaba', 'anapanamaban', 'napanamabana', 'apanamabanan']
    >>> all_rotations(5)
    Traceback (most recent call last):
        ...
    TypeError: The parameter s type must be str.
    """
    if not isinstance(s, str):
        raise TypeError("The parameter s type must be str.")

    return [s[i:] + s[:i] for i in range(len(s))]


def bwt_transform(s: str) -> BWTTransformDict:
    """
    :param s: BWT 算法使用的字符串
    :return: 由排序后各循环移位行的末字符组成的字符串，以及原字符串在排序后
        循环移位列表中的索引
    :raises TypeError: 参数 s 的类型不是 str 时引发
    :raises ValueError: 参数 s 为空时引发
    示例：

    >>> bwt_transform("^BANANA")
    {'bwt_string': 'BNN^AAA', 'idx_original_string': 6}
    >>> bwt_transform("a_asa_da_casa")
    {'bwt_string': 'aaaadss_c__aa', 'idx_original_string': 3}
    >>> bwt_transform("panamabanana")
    {'bwt_string': 'mnpbnnaaaaaa', 'idx_original_string': 11}
    >>> bwt_transform(4)
    Traceback (most recent call last):
        ...
    TypeError: The parameter s type must be str.
    >>> bwt_transform('')
    Traceback (most recent call last):
        ...
    ValueError: The parameter s must not be empty.
    """
    if not isinstance(s, str):
        raise TypeError("The parameter s type must be str.")
    if not s:
        raise ValueError("The parameter s must not be empty.")

    rotations = all_rotations(s)
    rotations.sort()  # 按字母顺序对循环移位列表排序
    # 构造由各循环移位结果的末字符组成的字符串
    response: BWTTransformDict = {
        "bwt_string": "".join([word[-1] for word in rotations]),
        "idx_original_string": rotations.index(s),
    }
    return response


def reverse_bwt(bwt_string: str, idx_original_string: int) -> str:
    """
    :param bwt_string: BWT 算法执行后返回的字符串
    :param idx_original_string: 生成 bwt_string 的原字符串在排序后循环移位列表中
        从 0 开始的索引
    :return: 执行 BWT 时用于生成 bwt_string 的原字符串
    :raises TypeError: 参数 bwt_string 的类型不是 str 时引发
    :raises ValueError: 参数 bwt_string 为空时引发
    :raises TypeError: idx_original_string 不是 int 且无法转换为 int 时引发
    :raises ValueError: idx_original_string 小于 0 或大于 len(bwt_string) - 1 时引发

    >>> reverse_bwt("BNN^AAA", 6)
    '^BANANA'
    >>> reverse_bwt("aaaadss_c__aa", 3)
    'a_asa_da_casa'
    >>> reverse_bwt("mnpbnnaaaaaa", 11)
    'panamabanana'
    >>> reverse_bwt(4, 11)
    Traceback (most recent call last):
        ...
    TypeError: The parameter bwt_string type must be str.
    >>> reverse_bwt("", 11)
    Traceback (most recent call last):
        ...
    ValueError: The parameter bwt_string must not be empty.
    >>> reverse_bwt("mnpbnnaaaaaa", "asd") # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    TypeError: The parameter idx_original_string type must be int or passive
    of cast to int.
    >>> reverse_bwt("mnpbnnaaaaaa", -1)
    Traceback (most recent call last):
        ...
    ValueError: The parameter idx_original_string must not be lower than 0.
    >>> reverse_bwt("mnpbnnaaaaaa", 12) # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    ValueError: The parameter idx_original_string must be lower than
    len(bwt_string).
    >>> reverse_bwt("mnpbnnaaaaaa", 11.0)
    'panamabanana'
    >>> reverse_bwt("mnpbnnaaaaaa", 11.4)
    'panamabanana'
    """
    if not isinstance(bwt_string, str):
        raise TypeError("The parameter bwt_string type must be str.")
    if not bwt_string:
        raise ValueError("The parameter bwt_string must not be empty.")
    try:
        idx_original_string = int(idx_original_string)
    except ValueError:
        raise TypeError(
            "The parameter idx_original_string type must be int or passive"
            " of cast to int."
        )
    if idx_original_string < 0:
        raise ValueError("The parameter idx_original_string must not be lower than 0.")
    if idx_original_string >= len(bwt_string):
        raise ValueError(
            "The parameter idx_original_string must be lower than len(bwt_string)."
        )

    ordered_rotations = [""] * len(bwt_string)
    for _ in range(len(bwt_string)):
        for i in range(len(bwt_string)):
            ordered_rotations[i] = bwt_string[i] + ordered_rotations[i]
        ordered_rotations.sort()
    return ordered_rotations[idx_original_string]


if __name__ == "__main__":
    entry_msg = "Provide a string that I will generate its BWT transform: "
    s = input(entry_msg).strip()
    result = bwt_transform(s)
    print(
        f"Burrows Wheeler transform for string '{s}' results "
        f"in '{result['bwt_string']}'"
    )
    original_string = reverse_bwt(result["bwt_string"], result["idx_original_string"])
    print(
        f"Reversing Burrows Wheeler transform for entry '{result['bwt_string']}' "
        f"we get original string '{original_string}'"
    )
