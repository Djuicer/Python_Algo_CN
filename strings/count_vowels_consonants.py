def count_vowels_and_consonants(text: str) -> tuple[int, int]:
    """
        统计给定字符串中的元音和辅音数量。

        忽略非字母字符。

        参数：
            text (str): 输入字符串。

        返回：
            tuple[int, int]: 包含 (vowel_count,
    consonant_count) 的元组。
     示例：
        >>> count_vowels_and_consonants("Hello World")
        (3, 7)
        >>> count_vowels_and_consonants("AEIOU")
        (5, 0)
        >>> count_vowels_and_consonants("bcdf")
        (0, 4)
        >>> count_vowels_and_consonants("")
        (0, 0)
    """
    vowels = set("aeiouAEIOU")
    vowel_count = 0
    consonant_count = 0

    for char in text:
        if char.isalpha():
            if char in vowels:
                vowel_count += 1
            else:
                consonant_count += 1

    return vowel_count, consonant_count
