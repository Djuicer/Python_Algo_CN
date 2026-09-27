"""
Project Euler Problem 87: https://projecteuler.net/problem=87

可表示为一个素数平方、一个素数立方与一个素数四次幂之和的最小数是 28。
事实上，五十以下恰好有四个数能以这种方式表示：

28 = 22 + 23 + 24
33 = 32 + 23 + 24
49 = 52 + 23 + 24
47 = 22 + 33 + 24

五千万以下有多少个数可表示为一个素数平方、一个素数立方与一个素数四次幂之和？
"""


def solution(limit: int = 50000000) -> int:
    """
    返回小于 limit 且可表示为一个素数平方、一个素数立方与一个素数四次幂之和的整数数量。
    >>> solution(50)
    4
    """
    ret = set()
    prime_square_limit = int((limit - 24) ** (1 / 2))

    primes = set(range(3, prime_square_limit + 1, 2))
    primes.add(2)
    for p in range(3, prime_square_limit + 1, 2):
        if p not in primes:
            continue
        primes.difference_update(set(range(p * p, prime_square_limit + 1, p)))

    for prime1 in primes:
        square = prime1 * prime1
        for prime2 in primes:
            cube = prime2 * prime2 * prime2
            if square + cube >= limit - 16:
                break
            for prime3 in primes:
                tetr = prime3 * prime3 * prime3 * prime3
                total = square + cube + tetr
                if total >= limit:
                    break
                ret.add(total)

    return len(ret)


if __name__ == "__main__":
    print(f"{solution() = }")
