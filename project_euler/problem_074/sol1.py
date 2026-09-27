"""
Project Euler Problem 74: https://projecteuler.net/problem=74

数 145 因其各位数字的阶乘之和等于 145 而广为人知：

1! + 4! + 5! = 1 + 24 + 120 = 145

可能较少有人知道，169 会产生回到 169 的最长数字链；事实证明仅存在以下三个循环：

169 → 363601 → 1454 → 169
871 → 45361 → 871
872 → 45362 → 872

不难证明，每个起始数最终都会陷入循环。例如：

69 → 363600 → 1454 → 169 → 363601 (→ 1454)
78 → 45360 → 871 → 45361 (→ 871)
540 → 145 (→ 145)

从 69 开始会产生包含五个不重复项的链，而起始数低于一百万的最长不重复链包含六十项。

起始数低于一百万且恰好包含六十个不重复项的链有多少条？
"""

DIGIT_FACTORIALS = {
    "0": 1,
    "1": 1,
    "2": 2,
    "3": 6,
    "4": 24,
    "5": 120,
    "6": 720,
    "7": 5040,
    "8": 40320,
    "9": 362880,
}

CACHE_SUM_DIGIT_FACTORIALS = {145: 145}

CHAIN_LENGTH_CACHE = {
    145: 0,
    169: 3,
    36301: 3,
    1454: 3,
    871: 2,
    45361: 2,
    872: 2,
}


def sum_digit_factorials(n: int) -> int:
    """
    返回 n 的各位数字阶乘之和。
    >>> sum_digit_factorials(145)
    145
    >>> sum_digit_factorials(45361)
    871
    >>> sum_digit_factorials(540)
    145
    """
    if n in CACHE_SUM_DIGIT_FACTORIALS:
        return CACHE_SUM_DIGIT_FACTORIALS[n]
    ret = sum(DIGIT_FACTORIALS[let] for let in str(n))
    CACHE_SUM_DIGIT_FACTORIALS[n] = ret
    return ret


def chain_length(n: int, previous: set | None = None) -> int:
    """
    计算从 n 开始的不重复项链的长度。Previous 是包含链中先前成员的集合。
    >>> chain_length(10101)
    11
    >>> chain_length(555)
    20
    >>> chain_length(178924)
    39
    """
    previous = previous or set()
    if n in CHAIN_LENGTH_CACHE:
        return CHAIN_LENGTH_CACHE[n]
    next_number = sum_digit_factorials(n)
    if next_number in previous:
        CHAIN_LENGTH_CACHE[n] = 0
        return 0
    else:
        previous.add(n)
        ret = 1 + chain_length(next_number, previous)
        CHAIN_LENGTH_CACHE[n] = ret
        return ret


def solution(num_terms: int = 60, max_start: int = 1000000) -> int:
    """
    返回起始数低于一百万且恰好包含 n 个不重复项的链的数量。
    >>> solution(10,1000)
    28
    """
    return sum(1 for i in range(1, max_start) if chain_length(i) == num_terms)


if __name__ == "__main__":
    print(f"{solution() = }")
