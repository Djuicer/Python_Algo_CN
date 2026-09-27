"""
Project Euler Problem 173: https://projecteuler.net/problem=173

将方形薄片定义为带有方形“孔洞”的正方形边框，使其具有水平和垂直对称性。
例如，恰好使用三十二块方砖可以形成两种不同的方形薄片：

使用一百块方砖（不必一次用完）可以形成四十一种不同的方形薄片。

最多使用一百万块方砖可以形成多少种不同的方形薄片？
"""

from math import ceil, sqrt


def solution(limit: int = 1000000) -> int:
    """
    返回最多使用一百万块方砖时可形成的不同方形薄片数量。
    >>> solution(100)
    41
    """
    answer = 0

    for outer_width in range(3, (limit // 4) + 2):
        if outer_width**2 > limit:
            hole_width_lower_bound = max(ceil(sqrt(outer_width**2 - limit)), 1)
        else:
            hole_width_lower_bound = 1
        if (outer_width - hole_width_lower_bound) % 2:
            hole_width_lower_bound += 1

        answer += (outer_width - hole_width_lower_bound - 2) // 2 + 1

    return answer


if __name__ == "__main__":
    print(f"{solution() = }")
