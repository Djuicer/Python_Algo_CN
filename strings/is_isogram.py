"""
wiki: https://en.wikipedia.org/wiki/Heterogram_(literature)#Isograms
"""


def is_isogram(string: str) -> bool:
    """
    无重复字母词（Isogram）是没有重复字母的单词。
    例如 uncopyrightable 和 ambidextrously。
    >>> is_isogram('Uncopyrightable')
    True
    >>> is_isogram('allowance')
    False
    >>> is_isogram('copy1')
    Traceback (most recent call last):
     ...
    ValueError: String must only contain alphabetic characters.
    """
    if not all(x.isalpha() for x in string):
        raise ValueError("String must only contain alphabetic characters.")

    letters = string.lower()
    return len(letters) == len(set(letters))


if __name__ == "__main__":
    input_str = input("Enter a string ").strip()

    isogram = is_isogram(input_str)
    print(f"{input_str} is {'an' if isogram else 'not an'} isogram.")
