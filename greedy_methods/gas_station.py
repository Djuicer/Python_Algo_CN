"""
任务：
环形路线上有 n 个加油站，第 i 个加油站的
油量为 gas_quantities[i]。

汽车油箱容量无限，从第 i 个加油站
开到下一个加油站（第 i + 1 个）需要消耗 costs[i] 的油量。
从某个加油站出发时，油箱为空。

给定整数数组 gas_quantities 和 costs，如果可以沿顺时针方向
绕环形路线行驶一周，则返回出发
加油站的索引；否则返回 -1。
若存在解，则保证解唯一

Reference: https://leetcode.com/problems/gas-station/description

实现说明：
首先检查总油量是否足以完成全程；不足则返回 -1。
如果总油量充足，则一定存在有效的
起点，使汽车能够完成全程。
使用贪心策略计算每个加油站的油量净增量（gas_quantity - cost）。
遍历加油站时，如果累计净增量低于 0，
则从下一个加油站重新开始检查。

"""

from dataclasses import dataclass


@dataclass
class GasStation:
    gas_quantity: int
    cost: int


def get_gas_stations(
    gas_quantities: list[int], costs: list[int]
) -> tuple[GasStation, ...]:
    """
    返回由加油站组成的元组。

    Args:
        gas_quantities: 每个加油站可提供的油量
        costs: 从一个加油站开到下一个加油站所需的油量

    Returns:
        由加油站组成的元组

    >>> gas_stations = get_gas_stations([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])
    >>> len(gas_stations)
    5
    >>> gas_stations[0]
    GasStation(gas_quantity=1, cost=3)
    >>> gas_stations[-1]
    GasStation(gas_quantity=5, cost=2)
    """
    return tuple(
        GasStation(quantity, cost) for quantity, cost in zip(gas_quantities, costs)
    )


def can_complete_journey(gas_stations: tuple[GasStation, ...]) -> int:
    """
    返回能够完成全程的
    起始加油站索引。

    Args:
        gas_quantities [list]: 每个加油站可提供的油量
        cost [list]: 从一个加油站开到下一个加油站所需的油量

    Returns:
        start [int]: 完成全程所需的起始索引

    示例：
    >>> can_complete_journey(get_gas_stations([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]))
    3
    >>> can_complete_journey(get_gas_stations([2, 3, 4], [3, 4, 3]))
    -1
    """
    total_gas = sum(gas_station.gas_quantity for gas_station in gas_stations)
    total_cost = sum(gas_station.cost for gas_station in gas_stations)
    if total_gas < total_cost:
        return -1

    start = 0
    net = 0
    for i, gas_station in enumerate(gas_stations):
        net += gas_station.gas_quantity - gas_station.cost
        if net < 0:
            start = i + 1
            net = 0
    return start


if __name__ == "__main__":
    import doctest

    doctest.testmod()
