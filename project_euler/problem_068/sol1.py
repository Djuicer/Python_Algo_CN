"""
Project Euler Problem 68: https://projecteuler.net/problem=68

魔法五边环

题目说明：
考虑下面的“魔法”三边环，其中填入数字 1 到 6，并且每条线之和为九。

   4
    \
     3
    / \
   1 - 2 - 6
  /
 5

按顺时针方向，从外部节点数值最小的三元组开始（本例为 4,3,2），
每个解都可以被唯一描述。例如，上述解可由集合 4,3,2; 6,2,1; 5,1,3 描述。

该环可用四种不同总和完成：9, 10, 11 和 12，共有八个解。
总和    解集
9       4,2,3; 5,3,1; 6,1,2
9       4,3,2; 6,2,1; 5,1,3
10      2,3,5; 4,5,1; 6,1,3
10      2,5,3; 6,3,1; 4,1,5
11      1,4,6; 3,6,2; 5,2,4
11      1,6,4; 5,4,2; 3,2,6
12      1,5,6; 2,6,4; 3,4,5
12      1,6,5; 3,5,4; 2,4,6

连接每个三元组可形成 9 位字符串；三边环的最大字符串为 432621513。

使用数字 1 到 10，根据不同排列可形成 16 位和 17 位字符串。
“魔法”五边环所能形成的最大 16 位字符串是什么？
"""

from itertools import permutations


def solution(gon_side: int = 5) -> int:
    """
    找出“魔法”gon_side 边环的最大数字。

    gon_side 参数应在 [3, 5] 范围内，其他边数未经测试。

    >>> solution(3)
    432621513
    >>> solution(4)
    426561813732
    >>> solution()
    6531031914842725
    >>> solution(6)
    Traceback (most recent call last):
    ValueError: gon_side must be in the range [3, 5]
    """
    if gon_side < 3 or gon_side > 5:
        raise ValueError("gon_side must be in the range [3, 5]")

    # 由于结果是 16 位数，可知 10 位于外环
    # 将较大的数放在末尾，使它们不会成为第一个数
    small_numbers = list(range(gon_side + 1, 0, -1))
    big_numbers = list(range(gon_side + 2, gon_side * 2 + 1))

    for perm in permutations(small_numbers + big_numbers):
        numbers = generate_gon_ring(gon_side, list(perm))
        if is_magic_gon(numbers):
            return int("".join(str(n) for n in numbers))

    msg = f"Magic {gon_side}-gon ring is impossible"
    raise ValueError(msg)


def generate_gon_ring(gon_side: int, perm: list[int]) -> list[int]:
    """
    从排列状态生成 gon_side 边环。排列状态即去除所有重复项后的环。

    >>> generate_gon_ring(3, [4, 2, 3, 5, 1, 6])
    [4, 2, 3, 5, 3, 1, 6, 1, 2]
    >>> generate_gon_ring(5, [6, 5, 4, 3, 2, 1, 7, 8, 9, 10])
    [6, 5, 4, 3, 4, 2, 1, 2, 7, 8, 7, 9, 10, 9, 5]
    """
    result = [0] * (gon_side * 3)
    result[0:3] = perm[0:3]
    perm.append(perm[1])

    magic_number = 1 if gon_side < 5 else 2

    for i in range(1, len(perm) // 3 + magic_number):
        result[3 * i] = perm[2 * i + 1]
        result[3 * i + 1] = result[3 * i - 1]
        result[3 * i + 2] = perm[2 * i + 2]

    return result


def is_magic_gon(numbers: list[int]) -> bool:
    """
    检查解集是否为魔法 n 边环。
    检查第一个数是否为外环上的最小数，并检查列表中每 3 个数一组的和是否相等。

    >>> is_magic_gon([4, 2, 3, 5, 3, 1, 6, 1, 2])
    True
    >>> is_magic_gon([4, 3, 2, 6, 2, 1, 5, 1, 3])
    True
    >>> is_magic_gon([2, 3, 5, 4, 5, 1, 6, 1, 3])
    True
    >>> is_magic_gon([1, 2, 3, 4, 5, 6, 7, 8, 9])
    False
    >>> is_magic_gon([1])
    Traceback (most recent call last):
    ValueError: a gon ring should have a length that is a multiple of 3
    """
    if len(numbers) % 3 != 0:
        raise ValueError("a gon ring should have a length that is a multiple of 3")

    if min(numbers[::3]) != numbers[0]:
        return False

    total = sum(numbers[:3])

    return all(sum(numbers[i : i + 3]) == total for i in range(3, len(numbers), 3))


if __name__ == "__main__":
    print(solution())
