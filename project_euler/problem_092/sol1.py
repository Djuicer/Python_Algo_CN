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
    limit = num_digits * 81 + 1  # 最大可能数字平方和 + 1

    def digit_square_sum(n: int) -> int:
        total = 0
        while n:
            total += (n % 10) ** 2
            n //= 10
        return total

    # 预计算 1..limit-1 中的每个值最终是否到达 89
    # 所有中间链值都小于 limit，因为任意 k 位数的数字平方和至多为
    # k * 81 = limit - 1
    ends_at_89 = bytearray(limit)
    for i in range(1, limit):
        n = i
        while n not in (1, 89):
            n = digit_square_sum(n)
        ends_at_89[i] = n == 89

    # 对 (number - 1) 的十进制数字执行数位 DP
    # 将较短的数视为用零填充的字符串（例如 7 → "0000007"）是安全的，
    # 因为 0^2 = 0 对数字平方和没有贡献
    # dp_tight[s] / dp_free[s] = 当前数字平方和为 s，且其前缀相对于
    # (number - 1) 的对应前缀仍满足 ≤ / 已满足 < 的数字序列数量
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

    # 对所有最终到达 89 的数字平方和的计数求和
    # dss == 0 对应数字 0，应将其排除
    return sum(
        cnt
        for dss, cnt in (*dp_tight.items(), *dp_free.items())
        if 0 < dss < limit and ends_at_89[dss]
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(f"{solution() = }")
