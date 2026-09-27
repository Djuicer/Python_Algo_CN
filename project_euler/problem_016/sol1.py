"""
Problem 16: https://projecteuler.net/problem=16

2^15 = 32768，其各位数字之和为 3 + 2 + 7 + 6 + 8 = 26。

数 2^1000 的各位数字之和是多少？
"""


def solution(power: int = 1000) -> int:
    """返回数 2^power 的各位数字之和。
    >>> solution(1000)
    1366
    >>> solution(50)
    76
    >>> solution(20)
    31
    >>> solution(15)
    26
    """
    num = 2**power
    string_num = str(num)
    list_num = list(string_num)
    sum_of_num = 0

    for i in list_num:
        sum_of_num += int(i)

    return sum_of_num


if __name__ == "__main__":
    power = int(input("Enter the power of 2: ").strip())
    print("2 ^ ", power, " = ", 2**power)
    result = solution(power)
    print("Sum of the digits is: ", result)
