"""
Project Euler Problem 95: https://projecteuler.net/problem=95

亲和链

一个数的真约数是除该数本身之外的所有约数。例如，28 的真约数为 1, 2, 4, 7 和 14。
由于这些约数之和等于 28，所以称它为完全数。

有趣的是，220 的真约数之和为 284，而 284 的真约数之和为 220，形成一条由两个数
组成的链。因此，220 和 284 称为一对亲和数。

较长的链可能不太为人所知。例如，从 12496 开始可形成一条包含五个数的链：
    12496 -> 14288 -> 15472 -> 14536 -> 14264 (-> 12496 -> ...)

由于该链返回起点，所以称为亲和链。

找出所有元素均不超过一百万的最长亲和链中的最小成员。

解法执行以下步骤：
- 获取相关素数
- 遍历素数乘积组合并记录素因数，生成不超过最大数的所有非素数
- 计算每个数的因数和
- 遍历所得因数和以寻找最长链
"""

from math import isqrt


def generate_primes(max_num: int) -> list[int]:
    """
    计算不超过 `max_num` 的素数列表。

    >>> generate_primes(6)
    [2, 3, 5]
    """
    are_primes = [True] * (max_num + 1)
    are_primes[0] = are_primes[1] = False
    for i in range(2, isqrt(max_num) + 1):
        if are_primes[i]:
            for j in range(i * i, max_num + 1, i):
                are_primes[j] = False

    return [prime for prime, is_prime in enumerate(are_primes) if is_prime]


def multiply(
    chain: list[int],
    primes: list[int],
    min_prime_idx: int,
    prev_num: int,
    max_num: int,
    prev_sum: int,
    primes_degrees: dict[int, int],
) -> None:
    """
    遍历所有素数组合以生成非素数。

    >>> chain = [0] * 3
    >>> primes_degrees = {}
    >>> multiply(
    ...     chain=chain,
    ...     primes=[2],
    ...     min_prime_idx=0,
    ...     prev_num=1,
    ...     max_num=2,
    ...     prev_sum=0,
    ...     primes_degrees=primes_degrees,
    ... )
    >>> chain
    [0, 0, 1]
    >>> primes_degrees
    {2: 1}
    """

    min_prime = primes[min_prime_idx]
    num = prev_num * min_prime

    min_prime_degree = primes_degrees.get(min_prime, 0)
    min_prime_degree += 1
    primes_degrees[min_prime] = min_prime_degree

    new_sum = prev_sum * min_prime + (prev_sum + prev_num) * (min_prime - 1) // (
        min_prime**min_prime_degree - 1
    )
    chain[num] = new_sum

    for prime_idx in range(min_prime_idx, len(primes)):
        if primes[prime_idx] * num > max_num:
            break

        multiply(
            chain=chain,
            primes=primes,
            min_prime_idx=prime_idx,
            prev_num=num,
            max_num=max_num,
            prev_sum=new_sum,
            primes_degrees=primes_degrees.copy(),
        )


def find_longest_chain(chain: list[int], max_num: int) -> int:
    """
    找出最长链中的最小元素。

    >>> find_longest_chain(chain=[0, 0, 0, 0, 0, 0, 6], max_num=6)
    6
    """

    max_len = 0
    min_elem = 0
    for start in range(2, len(chain)):
        visited = {start}
        elem = chain[start]
        length = 1

        while elem > 1 and elem <= max_num and elem not in visited:
            visited.add(elem)
            elem = chain[elem]
            length += 1

        if elem == start and length > max_len:
            max_len = length
            min_elem = start

    return min_elem


def solution(max_num: int = 1000000) -> int:
    """
    对 <= `max_num` 的数字执行计算。

    >>> solution(10)
    6
    >>> solution(200000)
    12496
    """

    primes = generate_primes(max_num)
    chain = [0] * (max_num + 1)
    for prime_idx, prime in enumerate(primes):
        if prime**2 > max_num:
            break

        multiply(
            chain=chain,
            primes=primes,
            min_prime_idx=prime_idx,
            prev_num=1,
            max_num=max_num,
            prev_sum=0,
            primes_degrees={},
        )

    return find_longest_chain(chain=chain, max_num=max_num)


if __name__ == "__main__":
    print(f"{solution() = }")
