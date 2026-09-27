"""
Project Euler Problem 4: https://projecteuler.net/problem=4

最大回文乘积

回文数从前向后读和从后向前读都相同。两个 2 位数乘积得到的最大回文数是
9009 = 91 x 99。

求两个 3 位数乘积得到的最大回文数。

参考资料：
    - https://en.wikipedia.org/wiki/Palindromic_number
"""


def solution(n: int = 998001) -> int:
    """
    返回小于 n、且由两个 3 位数的乘积得到的最大回文数。

    >>> solution(20000)
    19591
    >>> solution(30000)
    29992
    >>> solution(40000)
    39893
    >>> solution(10000)
    Traceback (most recent call last):
        ...
    ValueError: That number is larger than our acceptable range.
    """

        # 获取下一个数
    for number in range(n - 1, 9999, -1):
        str_number = str(number)

        # 检查 'str_number' 是否为回文数
        if str_number == str_number[::-1]:
            divisor = 999

        # 如果 'number' 是两个 3 位数的乘积，则它就是答案；否则获取下一个数
            while divisor != 99:
                if (number % divisor == 0) and (len(str(number // divisor)) == 3.0):
                    return number
                divisor -= 1
    raise ValueError("That number is larger than our acceptable range.")


if __name__ == "__main__":
    print(f"{solution() = }")
