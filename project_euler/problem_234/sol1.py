"""
https://projecteuler.net/problem=234

对于整数 n ≥ 4，将 n 的下素数平方根 lps(n) 定义为不大于 √n 的最大素数，
将 n 的上素数平方根 ups(n) 定义为不小于 √n 的最小素数。

例如，lps(4) = 2 = ups(4), lps(1000) = 31, ups(1000) = 37。若整数 n ≥ 4
可被 lps(n) 和 ups(n) 中的一个整除，但不能同时被二者整除，则称 n 为半可整除数。

不超过 15 的半可整除数之和为 30，这些数是 8, 10 and 12。15 不是半可整除数，
因为它同时是 lps(15) = 3 和 ups(15) = 5 的倍数。再举一例，不超过 1000 的
92 个半可整除数之和为 34825。

求所有不超过 999966663333 的半可整除数之和。
"""

import math


def prime_sieve(n: int) -> list:
    """
    埃拉托斯特尼筛法（Sieve of Eratosthenes）。
    返回小于某个数的所有素数。
    https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
    >>> prime_sieve(3)
    [2]
    >>> prime_sieve(50)
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    """
    is_prime = [True] * n
    is_prime[0] = False
    is_prime[1] = False
    is_prime[2] = True

    for i in range(3, int(n**0.5 + 1), 2):
        index = i * 2
        while index < n:
            is_prime[index] = False
            index = index + i

    primes = [2]

    for i in range(3, n, 2):
        if is_prime[i]:
            primes.append(i)

    return primes


def solution(limit: int = 999_966_663_333) -> int:
    """
    计算不超过指定 limit 时的问题解。
    >>> solution(1000)
    34825

    >>> solution(10_000)
    1134942

    >>> solution(100_000)
    36393008
    """
    primes_upper_bound = math.floor(math.sqrt(limit)) + 100
    primes = prime_sieve(primes_upper_bound)

    matches_sum = 0
    prime_index = 0
    last_prime = primes[prime_index]

    while (last_prime**2) <= limit:
        next_prime = primes[prime_index + 1]

        lower_bound = last_prime**2
        upper_bound = next_prime**2

        # 获取可被 lps(current) 整除的数
        current = lower_bound + last_prime
        while upper_bound > current <= limit:
            matches_sum += current
            current += last_prime

        # 重置 upper_bound
        while (upper_bound - next_prime) > limit:
            upper_bound -= next_prime

        # 加上可被 ups(current) 整除的数
        current = upper_bound - next_prime
        while current > lower_bound:
            matches_sum += current
            current -= next_prime

        # 移除同时可被 ups 和 lps 整除的数
        current = 0
        while upper_bound > current <= limit:
            if current <= lower_bound:
                # 递增当前数
                current += last_prime * next_prime
                continue

            if current > limit:
                break

            # 由于该数曾被 ups 和 lps 各加入一次，因此减去两次
            matches_sum -= current * 2

            # 递增当前数
            current += last_prime * next_prime

        # 为下一对进行设置
        last_prime = next_prime
        prime_index += 1

    return matches_sum


if __name__ == "__main__":
    print(solution())
