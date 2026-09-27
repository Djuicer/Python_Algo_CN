"""
Project Euler Problem 111: https://projecteuler.net/problem=111

重复数字素数

首先注意，对于 10 位数字序列，M(4,d) 为 8 或 9。
先构造不超过 sqrt(n) 的素数列表，用于检查数字是否为素数，
然后遍历可能的数字组合并逐一检查是否为素数。

"""

from numpy import sqrt


def generate_primes(n: int):
    """
    计算不超过 n 的素数列表。

    >>> generate_primes(6)
    [2, 3, 5]
    """
    primes = [True] * (n + 1)
    primes[0] = primes[1] = False
    for i in range(2, int(sqrt(n + 1)) + 1):
        if primes[i]:
            j = i * i
            while j <= n:
                primes[j] = False
                j += i
    primes_list = []
    for i in range(2, len(primes)):
        if primes[i]:
            primes_list += [i]
    return primes_list


def is_prime(n, primes_all):
    """
    使用相对于 n 较小的素数列表 primes_all，检查整数 n 是否为素数。

    >>> is_prime(5, [2, 3])
    True
    """
    return all(n % p != 0 for p in primes_all)


def solution(n: int = 10000000000) -> int:
    """
    检查每个可能的组合是否为素数。


    >>> solution(10000)
    273700
    """
    primes_all = generate_primes(int(sqrt(n)) + 1)
    total = 0

    n_zeros = len(str(n)) - 3
    for i in range(1, 10):
        for j in range(1, 10):
            num = int(str(i) + "0" * n_zeros + str(j))
            if is_prime(num, primes_all):
                total += num

    one_digit = set()
    n_dig = len(str(n)) - 2
    for i in range(1, 10):
        for j in range(n_dig + 1):
            for k in range(10):
                num = int(str(i) * j + str(k) + str(i) * (n_dig - j))
                if is_prime(num, primes_all):
                    one_digit.add(i)
                    total += num

    n_dig = len(str(n)) - 3
    two_dig = {1, 2, 3, 4, 5, 6, 7, 8, 9} - one_digit
    for i in list(two_dig):  # main digit
        for j in range(n_dig + 1):
            for k in range(n_dig + 1 - j):
                for m1 in range(10):  # first changing digit
                    if m1 == 0 and j == 0:
                        continue
                    for m2 in range(10):  # second changing digit
                        num = int(
                            str(i) * j
                            + str(m1)
                            + str(i) * k
                            + str(m2)
                            + str(i) * (n_dig - j - k)
                        )
                        if is_prime(num, primes_all):
                            total += num

    return total


if __name__ == "__main__":
    print(f"{solution() = }")
