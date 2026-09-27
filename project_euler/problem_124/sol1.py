"""
Project Euler Problem 124: https://projecteuler.net/problem=124

有序根积

"""

from numpy import sqrt


def generate_primes(n: int) -> list[int]:
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


def generate_n(factors: list[int], n_max: int, n: int, res: set[int]):
    """
    生成所有可由 'factors' 以任意重数构造且不超过 'n_max' 的数字 n。

    >>> generate_n([2], 10, 1, set())
    """

    if len(factors) == 0:
        return
    fac = factors[0]
    factors_new = factors[1:]
    while n <= n_max:
        generate_n(factors_new, n_max, n, res)
        res.add(n)
        n *= fac
    return


def generate_rads(
    factors_all: list[int], n_max: int, n: int, res: dict, factors_prev: list[int]
):
    """
    生成所有 rad 及相关因数，例如 rad = factor_1 * ... * factor_k。
    输出存储在字典参数 'res' 中。

    >>> generate_rads([2], 10, 1, {}, [])
    """

    for i in range(len(factors_all)):
        f = factors_all[i]
        n_new = n * f
        if n_new > n_max:
            return
        # factors_new = factors_prev + [f]
        factors_new = [*factors_prev, f]
        res[n_new] = factors_new
        generate_rads(factors_all[(i + 1) :], n_max, n_new, res, factors_new)
    return


def solution(n_max: int = 100000, k: int = 10000) -> int:
    """
    遍历已排序的 'rads'，为 rad 生成所有数字 'n'。记录 n 的总数；当 k 落入某个 rad 时，
    对其所有 'n' 排序并选取对应的 n。

    >>> solution(10, 6)
    9
    >>> solution(10, 9)
    7
    """

    if k == 1:
        return 1

    primes = generate_primes(n_max)
    tot = 1
    rads_d: dict[int, list[int]] = {}
    factor_prev: list[int] = []
    generate_rads(primes, n_max, 1, rads_d, factor_prev)
    rads = sorted(rads_d)

    for r in rads:
        facts = rads_d[r]
        res: set[int] = set()
        generate_n(facts, n_max, r, res)
        res_len = len(res)
        if tot + res_len >= k:
            return sorted(res)[k - tot - 1]
        tot += res_len
    return -1


if __name__ == "__main__":
    print(f"{solution() = }")
