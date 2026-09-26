def find_smallest_and_largest_words(input_string: str) -> tuple:
    """
    按长度找出给定输入字符串中最短和最长的单词。

    参数：
        input_string (str): 待分析的输入字符串。

    返回：
        tuple: 包含找到的最短和最长单词的元组。
        若未找到单词，元组中的两个值均为 None。

    示例：
    >>> find_smallest_and_largest_words("My name is abc")
    ('My', 'name')

    >>> find_smallest_and_largest_words("Hello guys")
    ('guys', 'Hello')

    >>> find_smallest_and_largest_words("OnlyOneWord")
    ('OnlyOneWord', 'OnlyOneWord')
    """
    words = input_string.split()
    if not words:
        return None, None

    # 处理标点和特殊字符
    words = [word.strip(".,!?()[]{}") for word in words]

    smallest_word = min(words, key=len)
    largest_word = max(words, key=len)

    return smallest_word, largest_word


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    input_string = input("Enter a sentence:\n").strip()
    smallest, largest = find_smallest_and_largest_words(input_string)

    if smallest and largest:
        print(f"The smallest word in the given sentence is '{smallest}'")
        print(f"The largest word in the given sentence is '{largest}'")
    else:
        print("No words found in the input sentence.")
