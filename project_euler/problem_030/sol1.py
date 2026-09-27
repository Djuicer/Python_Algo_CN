"""题目说明（各位数字的五次幂）：https://projecteuler.net/problem=30

令人惊讶的是，只有三个数可以写成其各位数字四次幂之和：

1634 = 1^4 + 6^4 + 3^4 + 4^4
8208 = 8^4 + 2^4 + 0^4 + 8^4
9474 = 9^4 + 4^4 + 7^4 + 4^4
由于 1 = 1^4 不是一个和，因此不计入。

这些数之和为 1634 + 8208 + 9474 = 19316。

求所有可以写成其各位数字五次幂之和的数的总和。

9^5 = 59049
59049 * 7 = 413343（只有 6 位数字）
因此排除大于 999999 的数；
另外，59049 * 3 = 177147（超过三位数的条件），
所以数字 > 999，因而范围在 1000 到 1000000 之间。
"""

DIGITS_FIFTH_POWER = {str(digit): digit**5 for digit in range(10)}


def digits_fifth_powers_sum(number: int) -> int:
    """
    >>> digits_fifth_powers_sum(1234)
    1300
    """
    return sum(DIGITS_FIFTH_POWER[digit] for digit in str(number))


def solution() -> int:
    return sum(
        number
        for number in range(1000, 1000000)
        if number == digits_fifth_powers_sum(number)
    )


if __name__ == "__main__":
    print(solution())
