"""
Project Euler Problem 36
https://projecteuler.net/problem=36

题目说明：

双进制回文数
问题 36
十进制数 585 = 10010010012（二进制）在两种进制下都是回文数。

求一百万以下在十进制和二进制下都是回文数的所有数之和。

（请注意，任一进制下的回文数都不能包含前导零。）
"""

from __future__ import annotations


def is_palindrome(n: int | str) -> bool:
    """
    如果输入 n 是回文则返回 true，否则返回 false。n 可以是整数或字符串。

    >>> is_palindrome(909)
    True
    >>> is_palindrome(908)
    False
    >>> is_palindrome('10101')
    True
    >>> is_palindrome('10111')
    False
    """
    n = str(n)
    return n == n[::-1]


def solution(n: int = 1000000):
    """返回小于 n 且在十进制和二进制下都是回文数的所有数之和。

    >>> solution(1000000)
    872187
    >>> solution(500000)
    286602
    >>> solution(100000)
    286602
    >>> solution(1000)
    1772
    >>> solution(100)
    157
    >>> solution(10)
    25
    >>> solution(2)
    1
    >>> solution(1)
    0
    """
    total = 0

    for i in range(1, n):
        if is_palindrome(i) and is_palindrome(bin(i).split("b")[1]):
            total += i
    return total


if __name__ == "__main__":
    print(solution(int(str(input().strip()))))
