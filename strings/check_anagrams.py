"""
wiki: https://en.wikipedia.org/wiki/Anagram
"""

from collections import defaultdict


def check_anagrams(first_str: str, second_str: str) -> bool:
    """
    若两个字符串由相同字母组成，但排列不同，
    则互为字母异位词（Anagram），忽略大小写。
    >>> check_anagrams('Silent', 'Listen')
    True
    >>> check_anagrams('This is a string', 'Is this a string')
    True
    >>> check_anagrams('This is    a      string', 'Is     this a string')
    True
    >>> check_anagrams('There', 'Their')
    False
    """
    first_str = first_str.lower().strip()
    second_str = second_str.lower().strip()

    # 移除空白字符
    first_str = first_str.replace(" ", "")
    second_str = second_str.replace(" ", "")

    # 长度不同的字符串不互为字母异位词
    if len(first_str) != len(second_str):
        return False

    # count 的默认值应为 0
    count: defaultdict[str, int] = defaultdict(int)

    # 对于输入字符串中的每个字符，
    # 增加其对应的计数
    for i in range(len(first_str)):
        count[first_str[i]] += 1
        count[second_str[i]] -= 1

    return all(_count == 0 for _count in count.values())


if __name__ == "__main__":
    from doctest import testmod

    testmod()
    input_a = input("Enter the first string ").strip()
    input_b = input("Enter the second string ").strip()

    status = check_anagrams(input_a, input_b)
    print(f"{input_a} and {input_b} are {'' if status else 'not '}anagrams.")
