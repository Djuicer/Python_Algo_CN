# 字符集大小，称为基数
alphabet_size = 256
# 对字符串计算哈希值时使用的模数
modulus = 1000003


def rabin_karp(pattern: str, text: str) -> bool:
    """
    Rabin-Karp 算法用于在文本中寻找模式，
    复杂度为 O(nm)，同时处理多个模式时最有效，
    因为在预先计算哈希值后，能在 o(1) 时间内检查一组模式中
    是否有模式与某段文本匹配。

    这里是仅搜索单个模式的简单版本，
    但修改并不困难

    1) 计算模式的哈希值

    2) 逐字符遍历文本，移动一个与模式
        等长的窗口，
        计算窗口中文本的哈希值，与模式哈希值比较。
        仅在哈希值相同时检查内容是否相等
    """
    p_len = len(pattern)
    t_len = len(text)
    if p_len > t_len:
        return False

    p_hash = 0
    text_hash = 0
    modulus_power = 1

    # 计算模式和文本子串的哈希值
    for i in range(p_len):
        p_hash = (ord(pattern[i]) + p_hash * alphabet_size) % modulus
        text_hash = (ord(text[i]) + text_hash * alphabet_size) % modulus
        if i == p_len - 1:
            continue
        modulus_power = (modulus_power * alphabet_size) % modulus

    for i in range(t_len - p_len + 1):
        if text_hash == p_hash and text[i : i + p_len] == pattern:
            return True
        if i == t_len - p_len:
            continue
        # 计算滚动哈希：https://en.wikipedia.org/wiki/Rolling_hash
        text_hash = (
            (text_hash - ord(text[i]) * modulus_power) * alphabet_size
            + ord(text[i + p_len])
        ) % modulus
    return False


def test_rabin_karp() -> None:
    """
    >>> test_rabin_karp()
    Success.
    """
    # 测试 1)
    pattern = "abc1abc12"
    text1 = "alskfjaldsabc1abc1abc12k23adsfabcabc"
    text2 = "alskfjaldsk23adsfabcabc"
    assert rabin_karp(pattern, text1)
    assert not rabin_karp(pattern, text2)

    # 测试 2)
    pattern = "ABABX"
    text = "ABABZABABYABABX"
    assert rabin_karp(pattern, text)

    # 测试 3)
    pattern = "AAAB"
    text = "ABAAAAAB"
    assert rabin_karp(pattern, text)

    # 测试 4)
    pattern = "abcdabcy"
    text = "abcxabcdabxabcdabcdabcy"
    assert rabin_karp(pattern, text)

    # 测试 5)
    pattern = "Lü"
    text = "Lüsai"
    assert rabin_karp(pattern, text)
    pattern = "Lue"
    assert not rabin_karp(pattern, text)
    print("Success.")


if __name__ == "__main__":
    test_rabin_karp()
