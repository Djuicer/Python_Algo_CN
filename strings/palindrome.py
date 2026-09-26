# 判断字符串是否为回文的算法

from timeit import timeit

test_data = {
    "MALAYALAM": True,
    "String": False,
    "rotor": True,
    "level": True,
    "A": True,
    "BB": True,
    "ABC": False,
    "amanaplanacanalpanama": True,  # "a man a plan a canal panama"
    "abcdba": False,
    "AB": False,
}
# 确保测试数据有效
assert all((key == key[::-1]) == value for key, value in test_data.items())


def is_palindrome(s: str) -> bool:
    """
    s 是回文时返回 True，否则返回 False。

    >>> all(is_palindrome(key) == value for key, value in test_data.items())
    True
    """

    start_i = 0
    end_i = len(s) - 1
    while start_i < end_i:
        if s[start_i] == s[end_i]:
            start_i += 1
            end_i -= 1
        else:
            return False
    return True


def is_palindrome_traversal(s: str) -> bool:
    """
    s 是回文时返回 True，否则返回 False。

    >>> all(is_palindrome_traversal(key) == value for key, value in test_data.items())
    True
    """
    end = len(s) // 2
    n = len(s)

    # 只需遍历到字符串长度的一半，
    # 因为可以通过第 i 个索引
    # 访问倒数第 i 个元素。
    # 例如：[0,1,2,3,4,5] 的第 4 个索引可借助
    # 第 1 个索引访问（i==n-i-1），
    # 其中 n 为字符串长度
    return all(s[i] == s[n - i - 1] for i in range(end))


def is_palindrome_recursive(s: str) -> bool:
    """
    s 是回文时返回 True，否则返回 False。

    >>> all(is_palindrome_recursive(key) == value for key, value in test_data.items())
    True
    """
    if len(s) <= 1:
        return True
    if s[0] == s[len(s) - 1]:
        return is_palindrome_recursive(s[1:-1])
    else:
        return False


def is_palindrome_slice(s: str) -> bool:
    """
    s 是回文时返回 True，否则返回 False。

    >>> all(is_palindrome_slice(key) == value for key, value in test_data.items())
    True
    """
    return s == s[::-1]


def is_palindrome_ignore_case_and_spaces(s: str) -> bool:
    """
    忽略大小写、空格和标点后，若 s 是回文则返回 True。
    否则返回 False。

    >>> is_palindrome_ignore_case_and_spaces("A man a plan a canal Panama")
    True
    >>> is_palindrome_ignore_case_and_spaces("Was it a car or a cat I saw?")
    True
    >>> is_palindrome_ignore_case_and_spaces("Hello World")
    False
    >>> is_palindrome_ignore_case_and_spaces("Never Odd or Even")
    True
    >>> is_palindrome_ignore_case_and_spaces("")
    True
    """
    s = "".join(char.lower() for char in s if char.isalnum())
    return s == s[::-1]


test_data_ignore_case_and_spaces = {
    "A man a plan a canal Panama": True,
    "Was it a car or a cat I saw?": True,
    "Hello World": False,
    "Never Odd or Even": True,
    "": True,
}


def benchmark_function(name: str) -> None:
    stmt = f"all({name}(key) == value for key, value in test_data.items())"
    setup = f"from __main__ import test_data, {name}"
    number = 500000
    result = timeit(stmt=stmt, setup=setup, number=number)
    print(f"{name:<35} finished {number:,} runs in {result:.5f} seconds")


if __name__ == "__main__":
    for key, value in test_data.items():
        assert is_palindrome(key) == is_palindrome_recursive(key)
        assert is_palindrome(key) == is_palindrome_slice(key)
        print(f"{key:21} {value}")
    for key, value in test_data_ignore_case_and_spaces.items():
        assert is_palindrome_ignore_case_and_spaces(key) == value
    print("a man a plan a canal panama")

    # finished 500,000 runs in 0.46793 seconds
    benchmark_function("is_palindrome_slice")
    # finished 500,000 runs in 0.85234 seconds
    benchmark_function("is_palindrome")
    # finished 500,000 runs in 1.32028 seconds
    benchmark_function("is_palindrome_recursive")
    # finished 500,000 runs in 2.08679 seconds
    benchmark_function("is_palindrome_traversal")
    # finished 500,000 runs in 4.27493 seconds
    benchmark_function("is_palindrome_ignore_case_and_spaces")
