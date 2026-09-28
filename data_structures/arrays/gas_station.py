from typing import NamedTuple


class GasStation(NamedTuple):
    gas: int  # Amount 的 燃料 可用 在 此 燃料 station
    cost: int  # Cost 的 燃料 所需 到 drive 到 下一个 station


def can_complete_circuit(gas_stations: list[GasStation]) -> int:
    """
    查找 起始 station 索引 到 complete circuit,
    或 返回值 -1 如果 不 可能。
    参数：
      gas_stations (列表[GasStation]): 列表 的 燃料 stations 带有 燃料 并且 cost。
    返回值：
      该索引 的 起始 station，或 -1 如果 没有 解 存在。
    示例：
    >>> GS = GasStation
    >>> test_stations = (
    ...     [GS(1, 3), GS(2, 4), GS(3, 5), GS(4, 1), GS(5, 2)],
    ...     [GS(2, 3), GS(3, 4), GS(4, 3)],
    ...     [GS(5, 4), GS(1, 4), GS(2, 1), GS(3, 5), GS(4, 1)]
    ... )
    >>> can_complete_circuit(test_stations[0])
    3
    >>> can_complete_circuit(test_stations[1])
    -1
    >>> can_complete_circuit(test_stations[2])
    4
    """
    total_gas = sum(station.gas - station.cost for station in gas_stations)
    current_gas: int = 0
    start_station = 0
    for i, gas_station in enumerate(gas_stations):
        needed_gas = gas_station.gas - gas_station.cost
        total_gas += needed_gas
        current_gas += needed_gas
        if current_gas < 0:
            start_station = i + 1
            current_gas = 0
    if total_gas < 0:
        return -1
    return start_station


# 示例 usage 带有 doctests
if __name__ == "__main__":
    import doctest

    doctest.testmod()
