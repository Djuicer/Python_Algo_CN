from string import ascii_uppercase


def mixed_keyword(
    keyword: str, plaintext: str, verbose: bool = False, alphabet: str = ascii_uppercase
) -> str:
    """
    For keyword: hello

    H E L O
    A B C D
    F G I J
    K M N P
    Q R S T
    U V W X
    Y Z
    and map vertically

    >>> mixed_keyword("college", "UNIVERSITY", True)  # doctest: +NORMALIZE_WHITESPACE
    {'A': 'C', 'B': 'A', 'C': 'I', 'D': 'P', 'E': 'U', 'F': 'Z', 'G': 'O', 'H': 'B',
     'I': 'J', 'J': 'Q', 'K': 'V', 'L': 'L', 'M': 'D', 'N': 'K', 'O': 'R', 'P': 'W',
     'Q': 'E', 'R': 'F', 'S': 'M', 'T': 'S', 'U': 'X', 'V': 'G', 'W': 'H', 'X': 'N',
     'Y': 'T', 'Z': 'Y'}
    'XKJGUFMJST'

    >>> mixed_keyword("college", "UNIVERSITY", False)  # doctest: +NORMALIZE_WHITESPACE
    'XKJGUFMJST'
    """
    keyword = keyword.upper()
    plaintext = plaintext.upper()
    alphabet_set = set(alphabet)

    # 创建关键字中不重复字符的列表——其顺序决定如何将明文字符映射到密文
    unique_chars = []
    for char in keyword:
        if char in alphabet_set and char not in unique_chars:
            unique_chars.append(char)
    # 不重复字符的数量决定行数
    num_unique_chars_in_keyword = len(unique_chars)

    # 创建字母表的移位版本
    shifted_alphabet = unique_chars + [
        char for char in alphabet if char not in unique_chars
    ]

    # 将移位后的字母表拆分为多行，创建修改后的字母表
    modified_alphabet = [
        shifted_alphabet[k : k + num_unique_chars_in_keyword]
        for k in range(0, 26, num_unique_chars_in_keyword)
    ]

    # 将字母表字符映射到修改后的字母表字符，纵向遍历修改后的字母表（先按列）
    mapping = {}
    letter_index = 0
    for column in range(num_unique_chars_in_keyword):
        for row in modified_alphabet:
            # 如果当前行（最后一行）过短，则退出循环
            if len(row) <= column:
                break

            # 将当前字母映射到修改后字母表中的字母
            mapping[alphabet[letter_index]] = row[column]
            letter_index += 1

    if verbose:
        print(mapping)
    # 将明文映射到修改后的字母表，生成加密文本
    return "".join(mapping.get(char, char) for char in plaintext)


if __name__ == "__main__":
    # 用法示例
    print(mixed_keyword("college", "UNIVERSITY"))
