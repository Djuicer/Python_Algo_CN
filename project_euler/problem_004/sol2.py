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
    """

    answer = 0
    for i in range(999, 99, -1):  # 三位数的范围从 999 递减到 100
        for j in range(999, 99, -1):
            product_string = str(i * j)
            if product_string == product_string[::-1] and i * j < n:
                answer = max(answer, i * j)
    return answer


if __name__ == "__main__":
    print(f"{solution() = }")
