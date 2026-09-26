# ruff: noqa: RUF002 -- ambiguous-unicode-character-docstring
from __future__ import annotations


def wheatstone_solver(
    resistance_1: float, resistance_2: float, resistance_3: float
) -> float:
    r"""
    计算惠斯通电桥电路中的未知电阻（Rx）。

    惠斯通电桥是一种通过平衡桥式电路两臂来精确测量未知电阻的电路。

    已知电桥中的另外三个电阻时，此函数计算 Rx。当连接在两个分压器中点之间的
    检流计中没有电流流过时，称电桥达到平衡。
    * # https://en.wikipedia.org/wiki/Wheatstone_bridge

    电路图：

         R1         R2
      +--/\/\/--+--/\/\/--+
      |         |         |
     Vin       Vg        Vout
      |         |         |
      +--/\/\/--+--/\/\/--+
         R3        Rx

    平衡条件：
      R1 / R2 = R3 / R4

    此求解器使用平衡电桥公式：
    Rx = (R2/R1) × R3

    参数：
        resistance_1 (R1): 第一个已知电阻
        resistance_2 (R2): 第二个已知电阻
        resistance_3 (R3): 第三个已知电阻

    返回值：
        float: 计算得到的未知电阻（Rx）

      应用：
      - 测量未知电阻
      - 应变计电路
      - 传感器校准

    用法示例：
    >>> wheatstone_solver(resistance_1=2, resistance_2=4, resistance_3=5)
    10.0
    >>> wheatstone_solver(resistance_1=356, resistance_2=234, resistance_3=976)
    641.5280898876405
    >>> wheatstone_solver(resistance_1=2, resistance_2=-1, resistance_3=2)
    Traceback (most recent call last):
        ...
    ValueError: All resistance values must be positive
    >>> wheatstone_solver(resistance_1=0, resistance_2=0, resistance_3=2)
    Traceback (most recent call last):
        ...
    ValueError: All resistance values must be positive
    """

    if resistance_1 <= 0 or resistance_2 <= 0 or resistance_3 <= 0:
        raise ValueError("All resistance values must be positive")
    return float((resistance_2 / resistance_1) * resistance_3)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
