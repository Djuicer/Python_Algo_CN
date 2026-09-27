"""
使用动态规划查找给定上限以内的所有自恋数。

自恋数（也称为 Armstrong 数或加法完美数）是这样一个数：
其值等于自身各位数字的位数次幂之和。

例如，153 是自恋数，因为 153 = 1^3 + 5^3 + 3^3。

此实现使用带记忆化搜索（Memoization）的动态规划，高效计算数字的幂，
并查找指定上限以内的所有自恋数。

DP 优化会缓存 digit^power 计算。搜索许多数时，相同的数字幂计算会反复出现
（例如，153, 351, 135 都需要 1^3, 5^3, 3^3）。记忆化搜索避免了这些重复计算。

自恋数示例：
    一位数：0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    三位数：153, 370, 371, 407
    四位数：1634, 8208, 9474
    五位数：54748, 92727, 93084

Reference: https://en.wikipedia.org/wiki/Narcissistic_number
"""


def find_narcissistic_numbers(limit: int) -> list[int]:
    """
    使用动态规划查找给定上限以内的所有自恋数。

    此函数使用记忆化搜索缓存数字幂计算，避免在位数相同的不同数字之间重复计算。

    参数：
        limit: 搜索自恋数的上限（不包含）

    返回：
        list[int]: 小于 limit 的所有自恋数的有序列表

    示例：
        >>> find_narcissistic_numbers(10)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> find_narcissistic_numbers(160)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 153]
        >>> find_narcissistic_numbers(400)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371]
        >>> find_narcissistic_numbers(1000)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407]
        >>> find_narcissistic_numbers(10000)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407, 1634, 8208, 9474]
        >>> find_narcissistic_numbers(1)
        [0]
        >>> find_narcissistic_numbers(0)
        []
    """
    if limit <= 0:
        return []

    narcissistic_nums = []

    # 记忆化搜索：cache[(power, digit)] = digit^power
    # 这可以避免为不同数字重复计算相同的幂
    power_cache: dict[tuple[int, int], int] = {}

    def get_digit_power(digit: int, power: int) -> int:
        """使用记忆化搜索（DP 优化）获取 digit^power。"""
        if (power, digit) not in power_cache:
            power_cache[(power, digit)] = digit**power
        return power_cache[(power, digit)]

    # 检查上限以内的每个数
    for number in range(limit):
        # 计算位数
        num_digits = len(str(number))

        # 使用记忆化的幂计算各位数字幂之和
        remaining = number
        digit_sum = 0
        while remaining > 0:
            digit = remaining % 10
            digit_sum += get_digit_power(digit, num_digits)
            remaining //= 10

        # 检查是否为自恋数
        if digit_sum == number:
            narcissistic_nums.append(number)

    return narcissistic_nums


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # 演示动态规划方法
    print("Finding all narcissistic numbers up to 10000:")
    print("(Using memoization to cache digit power calculations)")
    print()

    narcissistic_numbers = find_narcissistic_numbers(10000)
    print(f"Found {len(narcissistic_numbers)} narcissistic numbers:")
    print(narcissistic_numbers)
