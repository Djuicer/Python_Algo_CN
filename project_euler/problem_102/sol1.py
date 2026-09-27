"""
在 Cartesian 平面上随机绘制三个不同的点，其中 -1000 ≤ x, y ≤ 1000，以形成三角形。

考虑以下两个三角形：

A(-340,495), B(-153,-910), C(835,-947)

X(-175,41), Y(-421,-714), Z(574,-645)

可以验证，三角形 ABC 包含原点，而三角形 XYZ 不包含原点。

triangles.txt（右键单击并选择 'Save Link/Target As...'）是一个 27K 文本文件，
包含一千个“随机”三角形的坐标。求内部包含原点的三角形数量。

注意：文件中的前两个示例表示上述两个三角形。
"""

from __future__ import annotations

from pathlib import Path


def vector_product(point1: tuple[int, int], point2: tuple[int, int]) -> int:
    """
    返回两个向量的二维叉积。
    >>> vector_product((1, 2), (-5, 0))
    10
    >>> vector_product((3, 1), (6, 10))
    24
    """
    return point1[0] * point2[1] - point1[1] * point2[0]


def contains_origin(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int) -> bool:
    """
    检查由点 A(x1, y1)、B(x2, y2)、C(x3, y3) 构成的三角形是否包含原点。
    >>> contains_origin(-340, 495, -153, -910, 835, -947)
    True
    >>> contains_origin(-175, 41, -421, -714, 574, -645)
    False
    """
    point_a: tuple[int, int] = (x1, y1)
    point_a_to_b: tuple[int, int] = (x2 - x1, y2 - y1)
    point_a_to_c: tuple[int, int] = (x3 - x1, y3 - y1)
    a: float = -vector_product(point_a, point_a_to_b) / vector_product(
        point_a_to_c, point_a_to_b
    )
    b: float = +vector_product(point_a, point_a_to_c) / vector_product(
        point_a_to_c, point_a_to_b
    )

    return a > 0 and b > 0 and a + b < 1


def solution(filename: str = "p102_triangles.txt") -> int:
    """
    求内部包含原点的三角形数量。
    >>> solution("test_triangles.txt")
    1
    """
    data: str = Path(__file__).parent.joinpath(filename).read_text(encoding="utf-8")

    triangles: list[list[int]] = []
    for line in data.strip().split("\n"):
        triangles.append([int(number) for number in line.split(",")])

    ret: int = 0
    triangle: list[int]

    for triangle in triangles:
        ret += contains_origin(*triangle)

    return ret


if __name__ == "__main__":
    print(f"{solution() = }")
