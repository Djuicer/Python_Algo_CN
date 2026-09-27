"""
Project Euler Problem 092: https://projecteuler.net/problem=92
平方数字链
不断求一个数各位数字的平方和以形成新数，直至出现先前见过的数，即可构成数字链。
例如：
44 → 32 → 13 → 10 → 1 → 1
85 → 89 → 145 → 42 → 20 → 4 → 16 → 37 → 58 → 89
因此，任何到达 1 或 89 的链都会陷入无限循环。最令人惊讶的是，每个起始数最终都会
到达 1 或 89。一千万以下有多少个起始数会到达 89？

参考资料：
    - https://en.wikipedia.org/wiki/Digital_root
    - https://en.wikipedia.org/wiki/Digit_DP
"""


def solution(number: int = 10_000_000) -> int:
    """
    返回 `number` 以下会在数字平方链中到达 89 的起始数数量。

    使用数位 DP，以 O(k * d_max * 10) 时间计算数量；当 number = 10^7 时约执行
    40 000 次运算，而无需显式遍历所有 `number` 值。

    关键观察：
    1. 对任意 n < number，digit_square_sum(n) ≤ num_digits * 81，
       因此只需在这个较小范围内预计算链的终点。
    2. 对 (number - 1) 的十进制数字进行数位 DP，统计 [0, number-1] 中具有各个可能
       数字平方和的整数数量，并按前缀是否仍受限（"tight"）或自由分组。
       数字平方和等于 0 的整数恰好只有 0 本身。

    >>> solution(100)
    80

    >>> solution(10_000_000)
    8581146
    """
    num_digits = len(str(number - 1)) if number > 1 else 1
    limit = num_digits * 81 + 1  # max possible digit-square sum + 1

    def digit_square_sum(n: int) -> int:
        total = 0
        while n:
            total += (n % 10) ** 2
            n //= 10
        return total

    # Precompute whether each value 1..limit-1 eventually reaches 89.
    # All intermediate chain values stay below limit because the digit-square
    # sum of any k-digit number is at most k * 81 = limit - 1.
    ends_at_89 = bytearray(limit)
    for i in range(1, limit):
        n = i
        while n not in (1, 89):
            n = digit_square_sum(n)
        ends_at_89[i] = n == 89

    # Digit DP over the decimal digits of (number - 1).
    # Treating shorter numbers as zero-padded strings (e.g. 7 → "0000007")
    # is safe because 0^2 = 0 contributes nothing to the digit-square sum.
    # dp_tight[s] / dp_free[s] = count of digit sequences whose running
    # digit-square sum is s and whose prefix is still ≤ / already < the
    # corresponding prefix of (number - 1).
    digits = [int(d) for d in str(number - 1)] if number > 1 else [0]

    dp_tight: dict[int, int] = {0: 1}
    dp_free: dict[int, int] = {}

    for lim in digits:
        new_tight: dict[int, int] = {}
        new_free: dict[int, int] = {}

        for dss, cnt in dp_tight.items():
            for d in range(lim + 1):
                new_val = dss + d * d
                if new_val < limit:
                    if d == lim:
                        new_tight[new_val] = new_tight.get(new_val, 0) + cnt
                    else:
                        new_free[new_val] = new_free.get(new_val, 0) + cnt

        for dss, cnt in dp_free.items():
            for d in range(10):
                new_val = dss + d * d
                if new_val < limit:
                    new_free[new_val] = new_free.get(new_val, 0) + cnt

        dp_tight, dp_free = new_tight, new_free

    # Sum counts for all digit-square sums that end at 89.
    # dss == 0 corresponds to the number 0, which is excluded.
    return sum(
        cnt
        for dss, cnt in (*dp_tight.items(), *dp_free.items())
        if 0 < dss < limit and ends_at_89[dss]
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(f"{solution() = }")
