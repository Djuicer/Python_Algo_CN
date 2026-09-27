"""
Project Euler Problem 86: https://projecteuler.net/problem=86

蜘蛛 S 位于一个尺寸为 6 x 5 x 3 的长方体房间一角，苍蝇 F 位于对角。
沿房间表面移动时，从 S 到 F 的最短“直线”距离为 10，路径如图所示。
￼
然而，对于任意给定长方体，最多有三条“最短”路径候选，而且最短路径的长度不一定为整数。

可以证明，当 M = 100 时，在忽略旋转、尺寸为整数且最大尺寸不超过 M x M x M 的
不同长方体中，恰有 2060 个的最短路径长度为整数。这是解数首次超过两千时的最小 M；
当 M = 99 时，解数为 1975。

找出使解数首次超过一百万的最小 M 值。

解法：
    将长方体的 3 条边长记为 a,b,c，使 1 <= a <= b <= c <= M。
    在概念上“展开”长方体并将各面铺在平面上，可以看出两个对角之间的最短距离为
    sqrt((a+b)^2 + c^2)。当且仅当 (a+b),c 构成勾股数的前 2 条边时，该距离为整数。

    第二个有用的观察是，无需对每个最大边长 M 单独计算最短距离为整数的长方体数量，
    而可在每次增加 M 时迭代计算。最大边长为 M-1 且满足该性质的长方体集合，
    是最大边长为 M 的对应集合的子集（边长 <= M-1 的长方体也满足 <= M）。
    要计算更大集合（对应 M）中的长方体数量，只需考虑至少有一条边长为 M 的长方体。
    由于边长已排序为 a <= b <= c，可令 c = M，再统计满足下列条件的 a,b 数对：
        sqrt((a+b)^2 + M^2) is integer
        1 <= a <= b <= M

    为统计满足这些条件的 (a,b) 数对数量，令 d = a+b。于是有：
        1 <= a <= b <= M  =>  2 <= d <= 2*M
                                   实际可将第二个等号改为严格不等号，
                                   因为 d = 2*M => d^2 + M^2 = 5M^2
                                              => 最短距离 = M * sqrt(5)
                                              => 不是整数。
        a + b = d => b = d - a
                 and a <= b
                  => a <= d/2
                also a <= M
                  => a <= min(M, d//2)

        a + b = d => a = d - b
                 and b <= M
                  => a >= d - M
                also a >= 1
                  => a >= max(1, d - M)

        因此 a 位于 range(max(1, d - M), min(M, d // 2) + 1)

    对给定 d，满足所需性质且 c = M、a + b = d 的长方体数量即该范围的长度：
        min(M, d // 2) + 1 - max(1, d - M).

    在以下代码中，d 为 sum_shortest_sides，M 为 max_cuboid_size。


"""

from math import sqrt


def solution(limit: int = 1000000) -> int:
    """
    返回使下述长方体数量超过一百万的最小 M：边长满足 1 <= a,b,c <= M，
    且两个对角顶点之间的最短距离为整数。
    >>> solution(100)
    24
    >>> solution(1000)
    72
    >>> solution(2000)
    100
    >>> solution(20000)
    288
    """
    num_cuboids: int = 0
    max_cuboid_size: int = 0
    sum_shortest_sides: int

    while num_cuboids <= limit:
        max_cuboid_size += 1
        for sum_shortest_sides in range(2, 2 * max_cuboid_size + 1):
            if sqrt(sum_shortest_sides**2 + max_cuboid_size**2).is_integer():
                num_cuboids += (
                    min(max_cuboid_size, sum_shortest_sides // 2)
                    - max(1, sum_shortest_sides - max_cuboid_size)
                    + 1
                )

    return max_cuboid_size


if __name__ == "__main__":
    print(f"{solution() = }")
