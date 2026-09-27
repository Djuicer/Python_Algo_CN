"""
Project Euler Problem 60: https://projecteuler.net/problem=60

# 题目说明：

素数 3, 7, 109 和 673 非常特别。任取其中两个素数，以任意顺序连接，结果始终是素数。
例如，取 7 和 109，7109 与 1097 都是素数。这四个素数之和 792，是具有该性质的
四素数集合中的最小和。找出具有如下性质的五素数集合的最小和：任意两个素数连接后
仍为素数。

# 解法说明：

暴力方法会检查所有 5 个素数的组合并判断其是否满足连接性质，但计算代价很高。
可改用回溯法构造满足连接性质的素数集合，并利用被 3 整除的性质排除部分候选值，
再通过记忆化避免重复的素数检查。代码使用参数 flag 表示当前处理的是模 3 余 1
还是余 2 的素数，从而缩小搜索空间。

## 利用被 3 整除的性质排除候选值：
考虑任意两个不能被 3 整除的素数 p1 和 p2。如果 p1 除以 3 余 1，p2 除以 3 余 2，
则连接所得数字 p1p2 能被 3 整除，因此不是素数。利用模运算性质可轻易证明这一点。
    考虑 p1 ≡ 1 (mod 3) 和 p2 ≡ 2 (mod 3)。定义 a1 = p1, b1 = 1, a2 = p2, b2 = 2。
    concat(p1, p2) = (p1 * 10^k + p2)，其中 k 是 p2 的位数。
    于是，(p1 * 10^k + p2) mod 3 = ((p1 * 10^k) + p2) mod 3
    由于 10^k mod 3 = 1，可得 (p1 * 1 + p2) mod 3 (ka mod 3 = kb mod 3)
    这意味着 (p1 + p2) mod 3 = (1 + 2) mod 3 = 0 (a1 + a2 mod 3 = b1 + b2 mod 3)

因此可以从搜索空间中排除这样的数对，更快得到解。本解法根据素数除以 3 的余数，
利用该性质将素数分成两个列表。这样只需检查各列表内部的组合，可显著减少检查次数。

## 记忆化：
使用字典存储连接数的素数检查结果。再次遇到相同连接数时，可直接查找结果而无需重算。

## 回溯：
使用递归函数构造素数集合。从空集开始逐个加入素数，每一步检查当前集合是否满足连接性质；
若满足则继续加入。达到包含 5 个素数的集合后，检查其和是否最小。

参考资料：
- [Modular Arithmetic Explanation](https://en.wikipedia.org/wiki/Modular_arithmetic)
- [Project Euler Forum Discussion](https://projecteuler.net/problem=60)
- [Prime Checking Optimization](https://en.wikipedia.org/wiki/Primality_test)
- [Backtracking Algorithm](https://en.wikipedia.org/wiki/Backtracking)
"""

from functools import cache

prime_mod_3_is_1_list: list[int] = [3, 7, 13, 19]
prime_mod_3_is_2_list: list[int] = [3, 5, 11, 17]

prime_pairs: dict[tuple, bool] = {}


@cache
def is_prime(num: int) -> bool:
    """
    使用 6k ± 1 优化高效检查素数。

    >>> is_prime(0)
    False
    >>> is_prime(1)
    False
    >>> is_prime(2)
    True
    >>> is_prime(3)
    True
    >>> is_prime(77)
    False
    >>> is_prime(673)
    True
    >>> is_prime(1097)
    True
    >>> is_prime(7109)
    True
    """

    if num < 2:
        return False
    if num in (2, 3):
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    # 检查不超过 sqrt(num) 的因数
    n_sqrt = int(num**0.5)
    for i in range(5, n_sqrt + 1, 6):
        if num % i == 0 or num % (i + 2) == 0:
            return False
    return True


def sum_digits(num: int) -> int:
    """
    返回 num 的各位数字之和。如果该和大于 10，则递归求结果的各位数字之和，
    直至得到一位数。

    >>> sum_digits(-18)
    Traceback (most recent call last):
        ...
    ValueError: num must be non-negative
    >>> sum_digits(0)
    0
    >>> sum_digits(5)
    5
    >>> sum_digits(79)
    7
    >>> sum_digits(999)
    9
    """
    if num < 0:
        raise ValueError("num must be non-negative")
    if num < 10:
        return num
    return sum_digits(sum(map(int, str(num))))


def is_concat(num1: int, num2: int) -> bool:
    """
    检查 num1+num2 与 num2+num1 的连接结果是否均为素数。
    使用记忆化将先前计算的结果存入 prime_pairs 字典。
    作用：用结果更新 prime_pairs 字典。为避免重复，仅将
    (min(num1, num2), max(num1, num2)) 存为键。

    >>> is_concat(3, 7)
    True
    >>> is_concat(1, 6)
    False
    >>> is_concat(7, 109)
    True
    >>> is_concat(13, 31)
    False
    """
    if num1 > num2:
        num1, num2 = num2, num1
    key = (num1, num2)
    if key in prime_pairs:
        return prime_pairs[key]
    concat1 = int(f"{num1}{num2}")
    concat2 = int(f"{num2}{num1}")
    result = is_prime(concat1) and is_prime(concat2)
    prime_pairs[key] = result
    return result


def add_prime(primes: list[int]) -> list[int]:
    """
    根据模 3 的值向输入素数列表添加一个新素数。
    作用：通过追加新素数来修改输入列表。

    >>> add_prime([3, 7, 13, 19])
    [3, 7, 13, 19, 31]
    >>> add_prime([3, 5, 11, 17])
    [3, 5, 11, 17, 23]
    >>> add_prime([3, 7, 13, 19, 31])
    [3, 7, 13, 19, 31, 37]
    """

    next_num = primes[-1] + 3  # 使用模运算得到同类素数
    while not is_prime(next_num):
        next_num += 3
    primes.append(next_num)
    return primes


def generate_primes(num_primes: int, flag: int = 1) -> list[int]:
    """
    根据模 3 的值生成前 num_primes 个素数的列表。

    >>> generate_primes(5, 1)
    [3, 7, 13, 19, 31]
    >>> generate_primes(5, 2)
    [3, 5, 11, 17, 23]
    """
    primes = prime_mod_3_is_1_list if flag == 1 else prime_mod_3_is_2_list
    while len(primes) < num_primes:
        primes = add_prime(primes)
    return primes


def solution(
    target_size: int = 5, prime_limit: int = 1000, flag: int = 1
) -> int | None:
    """
    搜索具有连接素数性质的素数集合。返回所找到最小集合的和，否则返回 None。

    >>> solution(3, 100, None)
    Traceback (most recent call last):
        ...
    ValueError: flag must be either 1 or 2
    >>> solution(4, 100, 1)
    792
    >>> solution(3, 100, 2)
    715
    >>> solution(5, 1000, 1)
    26033
    """
    if flag not in (1, 2):
        raise ValueError("flag must be either 1 or 2")
    primes = generate_primes(prime_limit, flag)

    def search(chain: tuple) -> tuple[int, ...] | None:
        """
        通过递归回溯搜索有效的素数集合。使用阈值确保不超过当前最小和。
        找到时返回有效集合，否则返回 None。

        >>> search((3,))
        (3, 7, 109, 673)
        >>> search((7,))
        (7, 109, 673, 3)
        """
        if len(chain) == target_size:
            return chain
        for p in primes:
            if p <= chain[-1]:
                continue
            if all(is_concat(p, c) for c in chain):
                result = search((*chain, p))
                if result:
                    return result
        return None

    for _, p in enumerate(primes):
        result = search((p,))
        if result and len(result) == target_size:
            return sum(result)

    return None  # 未找到有效集合


if __name__ == "__main__":
    print(f"{solution() = }")
