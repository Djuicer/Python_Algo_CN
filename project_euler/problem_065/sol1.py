"""
Project Euler Problem 65: https://projecteuler.net/problem=65

2 的平方根可以写成无限连分数。

sqrt(2) = 1 + 1 / (2 + 1 / (2 + 1 / (2 + 1 / (2 + ...))))

该无限连分数可写成 sqrt(2) = [1;(2)]，其中 (2) 表示 2 无限重复。
类似地，sqrt(23) = [4;(1,3,1,8)]。

事实证明，平方根连分数的部分值数列可给出最佳有理数近似。考虑 sqrt(2) 的渐近分数。

1 + 1 / 2 = 3/2
1 + 1 / (2 + 1 / 2) = 7/5
1 + 1 / (2 + 1 / (2 + 1 / 2)) = 17/12
1 + 1 / (2 + 1 / (2 + 1 / (2 + 1 / 2))) = 41/29

因此 sqrt(2) 的前十个渐近分数为：
1, 3/2, 7/5, 17/12, 41/29, 99/70, 239/169, 577/408, 1393/985, 3363/2378, ...

更令人惊讶的是，重要数学常数
e = [2;1,2,1,1,4,1,1,6,1,...,1,2k,1,...].

e 的渐近分数数列前十项为：
2, 3, 8/3, 11/4, 19/7, 87/32, 106/39, 193/71, 1264/465, 1457/536, ...

第 10 个渐近分数的分子各位数字之和为
1 + 4 + 5 + 7 = 17.

求 e 的连分数第 100 个渐近分数的分子各位数字之和。

-----

该解法主要是找出生成连分数分子的方程。对于第 i 个分子，规律为：

n_i = m_i * n_(i-1) + n_(i-2)

其中 m_i = e 的连分数表示中的第 i 个索引，n_0 = 1、n_1 = 2 为该表示的前 2 个数。

例如：
n_9 = 6 * 193 + 106 = 1264
1 + 2 + 6 + 4 = 13

n_10 = 1 * 193 + 1264 = 1457
1 + 4 + 5 + 7 = 17
"""


def sum_digits(num: int) -> int:
    """
    返回 num 的各位数字之和。

    >>> sum_digits(1)
    1
    >>> sum_digits(12345)
    15
    >>> sum_digits(999001)
    28
    """
    digit_sum = 0
    while num > 0:
        digit_sum += num % 10
        num //= 10
    return digit_sum


def solution(max_n: int = 100) -> int:
    """
    返回 e 的连分数第 max 个渐近分数的分子各位数字之和。

    >>> solution(9)
    13
    >>> solution(10)
    17
    >>> solution(50)
    91
    """
    pre_numerator = 1
    cur_numerator = 2

    for i in range(2, max_n + 1):
        temp = pre_numerator
        e_cont = 2 * i // 3 if i % 3 == 0 else 1
        pre_numerator = cur_numerator
        cur_numerator = e_cont * pre_numerator + temp

    return sum_digits(cur_numerator)


if __name__ == "__main__":
    print(f"{solution() = }")
