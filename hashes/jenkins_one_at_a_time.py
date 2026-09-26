"""
Bob Jenkins 哈希是一种快速的非密码学哈希函数，面向哈希表查找等通用场景。

https://en.wikipedia.org/wiki/Jenkins_hash_function
"""


def jenkins_one_at_a_time(key: str) -> int:
    """
    计算键的 Jenkins One-at-a-Time 哈希值。

    >>> jenkins_one_at_a_time("apple")
    2297466611
    >>> jenkins_one_at_a_time("test")
    1064684737
    >>> jenkins_one_at_a_time("")
    0
    """
    hash_value = 0
    mask = 0xFFFFFFFF
    key_bytes = key.encode("utf-8")

    for byte in key_bytes:
        hash_value = (hash_value + byte) & mask
        hash_value = (hash_value + (hash_value << 10)) & mask
        hash_value = (hash_value ^ (hash_value >> 6)) & mask

    hash_value = (hash_value + (hash_value << 3)) & mask
    hash_value = (hash_value ^ (hash_value >> 11)) & mask
    hash_value = (hash_value + (hash_value << 15)) & mask

    return hash_value


if __name__ == "__main__":
    import doctest

    doctest.testmod()
