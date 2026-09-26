def remove_duplicates(sentence: str) -> str:
    """
    移除句子中的重复项
    >>> remove_duplicates("Python is great and Java is also great")
    'Java Python also and great is'
    >>> remove_duplicates("Python   is      great and Java is also great")
    'Java Python also and great is'
    """
    return " ".join(sorted(set(sentence.split())))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
