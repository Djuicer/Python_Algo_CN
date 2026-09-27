"""
Problem 125: https://projecteuler.net/problem=125

回文数 595 很有趣，因为它可写成连续平方数之和：
6^2 + 7^2 + 8^2 + 9^2 + 10^2 + 11^2 + 12^2。

一千以下恰有十一个回文数可写成连续平方数之和，这些回文数之和为 4164。
注意，1 = 0^2 + 1^2 未计入，因为本题只考虑正整数的平方。

求所有小于 10^8、既是回文数又可写成连续平方数之和的数的总和。
"""

LIMIT = 10**8


def is_palindrome(n: int) -> bool:
    """
    检查一个整数是否为回文数。
    >>> is_palindrome(12521)
    True
    >>> is_palindrome(12522)
    False
    >>> is_palindrome(12210)
    False
    """
    if n % 10 == 0:
        return False
    s = str(n)
    return s == s[::-1]


def solution() -> int:
    """
    返回所有小于 1e8、既是回文数又可写成连续平方数之和的数的总和。
    """
    answer = set()
    first_square = 1
    sum_squares = 5
    while sum_squares < LIMIT:
        last_square = first_square + 1
        while sum_squares < LIMIT:
            if is_palindrome(sum_squares):
                answer.add(sum_squares)
            last_square += 1
            sum_squares += last_square**2
        first_square += 1
        sum_squares = first_square**2 + (first_square + 1) ** 2

    return sum(answer)


if __name__ == "__main__":
    print(solution())
