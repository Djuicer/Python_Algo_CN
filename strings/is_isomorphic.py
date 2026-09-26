def is_isomorphic(s: str, t: str) -> bool:
    """
    给定字符串 s 和 t，判断它们是否同构。
    https://en.wikipedia.org/wiki/Isomorphism
    https://leetcode.com/problems/isomorphic-strings/description/

    如果可以替换 s 中的字符得到 t，
    则 s 和 t 同构。

    每个字符的所有出现位置都必须替换为另一个相同字符，
    同时保持字符顺序。两个不同字符不能映射到
    同一字符，但字符可以映射到自身。


    >>> is_isomorphic("egg", "add")
    True
    >>> is_isomorphic("foo", "bar")
    False
    >>> is_isomorphic("paper", "title")
    True
    >>> is_isomorphic("ab", "aa")
    False
    """
    if len(s) != len(t):
        return False

    mapping: dict[str, str] = {}
    mapped = set()

    for char_s, char_t in zip(s, t):
        if char_s in mapping:
            if mapping[char_s] != char_t:
                return False
        else:
            if char_t in mapped:
                return False
            mapping[char_s] = char_t
            mapped.add(char_t)

    return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print(is_isomorphic("egg", "add"))  # True
