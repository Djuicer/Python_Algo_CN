"""
Project Euler Problem 187: https://projecteuler.net/problem=187

合数是至少包含两个素因数的数。
例如，15 = 3 x 5; 9 = 3 x 3; 12 = 2 x 2 x 3。

三十以下恰好包含两个（不要求互不相同）素因数的合数有十个：
4, 6, 9, 10, 14, 15, 21, 22, 25, 26。

有多少个合数 n < 10^8 恰好包含两个不要求互不相同的素因数？
"""

from math import isqrt


def slow_calculate_prime_numbers(max_number: int) -> list[int]:
    """
    返回 max_number 以下的素数。
    See: https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes

    >>> slow_calculate_prime_numbers(10)
    [2, 3, 5, 7]

    >>> slow_calculate_prime_numbers(2)
    []
    """

    # 为 max_number/2 以下的每个数保存一个布尔值的列表
    is_prime = [True] * max_number

    for i in range(2, isqrt(max_number - 1) + 1):
        if is_prime[i]:
            # 将 i 的所有倍数标记为非素数
            for j in range(i**2, max_number, i):
                is_prime[j] = False

    return [i for i in range(2, max_number) if is_prime[i]]


def calculate_prime_numbers(max_number: int) -> list[int]:
    """
    返回 max_number 以下的素数。
    See: https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes

    >>> calculate_prime_numbers(10)
    [2, 3, 5, 7]

    >>> calculate_prime_numbers(2)
    []
    """

    if max_number <= 2:
        return []

    # 为 max_number/2 以下的每个奇数保存一个布尔值的列表
    is_prime = [True] * (max_number // 2)

    for i in range(3, isqrt(max_number - 1) + 1, 2):
        if is_prime[i // 2]:
            # 使用列表切片将 i 的所有倍数标记为非素数
            is_prime[i**2 // 2 :: i] = [False] * (
                # 等同于：(max_number - (i**2)) // (2 * i) + 1
                # 但比 len(is_prime[i**2 // 2 :: i]) 更快
                len(range(i**2 // 2, max_number // 2, i))
            )

    return [2] + [2 * i + 1 for i in range(1, max_number // 2) if is_prime[i]]


def slow_solution(max_number: int = 10**8) -> int:
    """
    返回 max_number 以下恰好包含两个不要求互不相同素因数的合数数量。

    >>> slow_solution(30)
    10
    """

    prime_numbers = slow_calculate_prime_numbers(max_number // 2)

    semiprimes_count = 0
    left = 0
    right = len(prime_numbers) - 1
    while left <= right:
        while prime_numbers[left] * prime_numbers[right] >= max_number:
            right -= 1
        semiprimes_count += right - left + 1
        left += 1

    return semiprimes_count


def while_solution(max_number: int = 10**8) -> int:
    """
    返回 max_number 以下恰好包含两个不要求互不相同素因数的合数数量。

    >>> while_solution(30)
    10
    """

    prime_numbers = calculate_prime_numbers(max_number // 2)

    semiprimes_count = 0
    left = 0
    right = len(prime_numbers) - 1
    while left <= right:
        while prime_numbers[left] * prime_numbers[right] >= max_number:
            right -= 1
        semiprimes_count += right - left + 1
        left += 1

    return semiprimes_count


def solution(max_number: int = 10**8) -> int:
    """
    返回 max_number 以下恰好包含两个不要求互不相同素因数的合数数量。

    >>> solution(30)
    10
    """

    prime_numbers = calculate_prime_numbers(max_number // 2)

    semiprimes_count = 0
    right = len(prime_numbers) - 1
    for left in range(len(prime_numbers)):
        if left > right:
            break
        for r in range(right, left - 2, -1):
            if prime_numbers[left] * prime_numbers[r] < max_number:
                break
        right = r
        semiprimes_count += right - left + 1

    return semiprimes_count


def benchmark() -> None:
    """
    基准测试
    """
    # 运行性能基准测试……
    # slow_solution : 108.50874730000032
    # while_sol     : 28.09581200000048
    # solution      : 25.063097400000515

    from timeit import timeit

    print("Running performance benchmarks...")

    print(f"slow_solution : {timeit('slow_solution()', globals=globals(), number=10)}")
    print(f"while_sol     : {timeit('while_solution()', globals=globals(), number=10)}")
    print(f"solution      : {timeit('solution()', globals=globals(), number=10)}")


if __name__ == "__main__":
    print(f"Solution: {solution()}")
    benchmark()
