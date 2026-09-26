# https://en.wikipedia.org/wiki/Set_cover_problem

from dataclasses import dataclass
from operator import attrgetter


@dataclass
class Item:
    weight: int
    value: int

    @property
    def ratio(self) -> float:
        """
        返回物品的价值与重量之比。

        Returns:
            float: 物品的价值与重量之比。

        示例：
        >>> Item(10, 65).ratio
        6.5

        >>> Item(20, 100).ratio
        5.0

        >>> Item(30, 120).ratio
        4.0
        """
        return self.value / self.weight


def fractional_cover(items: list[Item], capacity: int) -> float:
    """
    求解分数覆盖问题（Fractional Cover Problem）。

    Args:
        items: 物品列表，每个物品都有 weight 和 value 属性。
        capacity: 背包可承受的最大重量。

    Returns:
        通过选取物品的一部分来填充背包容量，
        所能获得的最大价值。

    Raises:
        ValueError: capacity 为负数时抛出。

    示例：
    >>> fractional_cover((Item(10, 60), Item(20, 100), Item(30, 120)), capacity=50)
    240.0

    >>> fractional_cover([Item(20, 100), Item(30, 120), Item(10, 60)], capacity=25)
    135.0

    >>> fractional_cover([Item(10, 60), Item(20, 100), Item(30, 120)], capacity=60)
    280.0

    >>> fractional_cover(items=[Item(5, 30), Item(10, 60), Item(15, 90)], capacity=30)
    180.0

    >>> fractional_cover(items=[], capacity=50)
    0.0

    >>> fractional_cover(items=[Item(10, 60)], capacity=5)
    30.0

    >>> fractional_cover(items=[Item(10, 60)], capacity=1)
    6.0

    >>> fractional_cover(items=[Item(10, 60)], capacity=0)
    0.0

    >>> fractional_cover(items=[Item(10, 60)], capacity=-1)
    Traceback (most recent call last):
        ...
    ValueError: Capacity cannot be negative
    """
    if capacity < 0:
        raise ValueError("Capacity cannot be negative")

    total_value = 0.0
    remaining_capacity = capacity

    # 按价值与重量之比降序排列物品
    for item in sorted(items, key=attrgetter("ratio"), reverse=True):
        if remaining_capacity == 0:
            break

        weight_taken = min(item.weight, remaining_capacity)
        total_value += weight_taken * item.ratio
        remaining_capacity -= weight_taken

    return total_value


if __name__ == "__main__":
    import doctest

    if result := doctest.testmod().failed:
        print(f"{result} test(s) failed")
    else:
        print("All tests passed")
