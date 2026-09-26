"""
By @Shreya123714

https://en.wikipedia.org/wiki/Fuzzy_set
"""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class FuzzySet:
    """
    用于表示和操作三角模糊集合的类。
    属性：
        name: 模糊集合的名称或标签。
        left_boundary: 模糊集合的左边界。
        peak: 模糊集合的峰值（中心值）。
        right_boundary: 模糊集合的右边界。
    方法：
        membership(x): 计算输入 'x' 在模糊集合中的隶属度。
        union(other): 计算此模糊集合与另一模糊集合的并集。
        intersection(other): 计算此模糊集合与另一模糊集合的交集。
        complement(): 计算此模糊集合的补集（否定）。
        plot(): 绘制模糊集合的隶属函数。

    >>> sheru = FuzzySet("Sheru", 0.4, 1, 0.6)
    >>> sheru
    FuzzySet(name='Sheru', left_boundary=0.4, peak=1, right_boundary=0.6)
    >>> str(sheru)
    'Sheru: [0.4, 1, 0.6]'

    >>> siya = FuzzySet("Siya", 0.5, 1, 0.7)
    >>> siya
    FuzzySet(name='Siya', left_boundary=0.5, peak=1, right_boundary=0.7)

    # 补集运算
    >>> sheru.complement()
    FuzzySet(name='¬Sheru', left_boundary=0.4, peak=0.6, right_boundary=0)
    >>> siya.complement()  # doctest: +NORMALIZE_WHITESPACE
    FuzzySet(name='¬Siya', left_boundary=0.30000000000000004, peak=0.5,
     right_boundary=0)

    # 交集运算
    >>> siya.intersection(sheru)
    FuzzySet(name='Siya ∩ Sheru', left_boundary=0.5, peak=0.6, right_boundary=1.0)

    # 隶属度运算
    >>> sheru.membership(0.5)
    0.16666666666666663
    >>> sheru.membership(0.6)
    0.0

    # 并集运算
    >>> siya.union(sheru)
    FuzzySet(name='Siya U Sheru', left_boundary=0.4, peak=1.0, right_boundary=0.7)
    """

    name: str
    left_boundary: float
    peak: float
    right_boundary: float

    def __str__(self) -> str:
        """
        >>> FuzzySet("fuzzy_set", 0.1, 0.2, 0.3)
        FuzzySet(name='fuzzy_set', left_boundary=0.1, peak=0.2, right_boundary=0.3)
        """
        return (
            f"{self.name}: [{self.left_boundary}, {self.peak}, {self.right_boundary}]"
        )

    def complement(self) -> FuzzySet:
        """
        计算此模糊集合的补集（否定）。
        返回：
            FuzzySet: 表示补集的新模糊集合。

        >>> FuzzySet("fuzzy_set", 0.1, 0.2, 0.3).complement()
        FuzzySet(name='¬fuzzy_set', left_boundary=0.7, peak=0.9, right_boundary=0.8)
        """
        return FuzzySet(
            f"¬{self.name}",
            1 - self.right_boundary,
            1 - self.left_boundary,
            1 - self.peak,
        )

    def intersection(self, other) -> FuzzySet:
        """
        计算此模糊集合与另一模糊集合的交集。
        参数：
            other: 要与之求交集的另一模糊集合。
        返回：
            表示交集的新模糊集合。

        >>> FuzzySet("a", 0.1, 0.2, 0.3).intersection(FuzzySet("b", 0.4, 0.5, 0.6))
        FuzzySet(name='a ∩ b', left_boundary=0.4, peak=0.3, right_boundary=0.35)
        """
        return FuzzySet(
            f"{self.name} ∩ {other.name}",
            max(self.left_boundary, other.left_boundary),
            min(self.right_boundary, other.right_boundary),
            (self.peak + other.peak) / 2,
        )

    def membership(self, x: float) -> float:
        """
        计算输入 'x' 在模糊集合中的隶属度。
        返回：
            'x' 在模糊集合中的隶属度。

        >>> a = FuzzySet("a", 0.1, 0.2, 0.3)
        >>> a.membership(0.09)
        0.0
        >>> a.membership(0.1)
        0.0
        >>> a.membership(0.11)
        0.09999999999999995
        >>> a.membership(0.4)
        0.0
        >>> FuzzySet("A", 0, 0.5, 1).membership(0.1)
        0.2
        >>> FuzzySet("B", 0.2, 0.7, 1).membership(0.6)
        0.8
        """
        if x <= self.left_boundary or x >= self.right_boundary:
            return 0.0
        elif self.left_boundary < x <= self.peak:
            return (x - self.left_boundary) / (self.peak - self.left_boundary)
        elif self.peak < x < self.right_boundary:
            return (self.right_boundary - x) / (self.right_boundary - self.peak)
        msg = f"Invalid value {x} for fuzzy set {self}"
        raise ValueError(msg)

    def union(self, other) -> FuzzySet:
        """
        计算此模糊集合与另一模糊集合的并集。
        参数：
            other (FuzzySet): 要与之求并集的另一模糊集合。
        返回：
            FuzzySet: 表示并集的新模糊集合。

        >>> FuzzySet("a", 0.1, 0.2, 0.3).union(FuzzySet("b", 0.4, 0.5, 0.6))
        FuzzySet(name='a U b', left_boundary=0.1, peak=0.35, right_boundary=0.6)
        """
        return FuzzySet(
            f"{self.name} U {other.name}",
            min(self.left_boundary, other.left_boundary),
            (self.peak + other.peak) / 2,
            max(self.right_boundary, other.right_boundary),
        )

    def plot(self) -> None:
        """
        绘制模糊集合的隶属函数。
        """
        x = np.linspace(0, 1, 1000)
        y = [self.membership(xi) for xi in x]

        plt.plot(x, y, label=self.name)


if __name__ == "__main__":
    from doctest import testmod

    testmod()
    a = FuzzySet("A", 0, 0.5, 1)
    b = FuzzySet("B", 0.2, 0.7, 1)

    a.plot()
    b.plot()

    plt.xlabel("x")
    plt.ylabel("Membership")
    plt.legend()
    plt.show()

    union_ab = a.union(b)
    intersection_ab = a.intersection(b)
    complement_a = a.complement()

    union_ab.plot()
    intersection_ab.plot()
    complement_a.plot()

    plt.xlabel("x")
    plt.ylabel("Membership")
    plt.legend()
    plt.show()
