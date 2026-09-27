"""
Project Euler Problem 142: https://projecteuler.net/problem=142

完全平方数集合

求满足以下条件的最小 x + y + z：整数 x > y > z > 0，且
x + y, x - y, x + z, x - z, y + z, y - z 均为完全平方数。


将变量替换为 a、b、c，使 3 个条件自动满足：
a^2 = y - z
b^2 = x - y
c^2 = z + x

其余完全平方数条件为：
z + y = c^2 - b^2
y + x = a^2 + c^2
x - z = a^2 + b^2

然后遍历 a^2、b^2 和 c^2，检查组合是否满足全部 3 个条件。

总和 x + y + z = (a^2 - b^2 + 3c^2) / 2，因此若该和已大于找到的总和，
则终止 c^2 的循环。

"""


def solution(number_of_terms: int = 3) -> int | None:
    """

    遍历 a、b、c 的组合并保存最小总和。
    只有一项时，解为 x = 1。
    有两项时，解为 x = 5, y = 4。

    >>> solution(1)
    1
    >>> solution(2)
    9
    """

    if number_of_terms == 1:
        return 1
    if number_of_terms == 2:
        return 9

    n_max = 2500
    squares: list[int] = []

    for a in range(n_max + 1):
        squares += [a * a]
    squares_set = set(squares)

    min_sum = None
    for a in range(1, len(squares)):
        a_sq = squares[a]
        for b in range(1, len(squares)):
            b_sq = squares[b]
            if a_sq + b_sq not in squares_set:
                continue
            for c in range(max(a, b) + 1, len(squares)):
                c_sq = squares[c]
                # 如果 x + y + z 已大于 min_sum，则终止循环
                if min_sum is not None and (a_sq - b_sq + 3 * c_sq) // 2 > min_sum:
                    break
                if (c_sq - b_sq in squares_set) and (a_sq + c_sq in squares_set):
                    x2, y2, z2 = (
                        a_sq + b_sq + c_sq,
                        a_sq - b_sq + c_sq,
                        c_sq - a_sq - b_sq,
                    )
                    if z2 > 0 and x2 % 2 == 0 and y2 % 2 == 0 and z2 % 2 == 0:
                        sum_ = (x2 + y2 + z2) // 2
                        min_sum = sum_ if min_sum is None else min(min_sum, sum_)

    return min_sum


if __name__ == "__main__":
    print(f"{solution() = }")
