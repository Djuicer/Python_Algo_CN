# https://en.wikipedia.org/wiki/Coulomb%27s_law

from __future__ import annotations

COULOMBS_CONSTANT = 8.988e9  # 单位 = N * m^s * C^-2


def couloumbs_law(
    force: float, charge1: float, charge2: float, distance: float
) -> dict[str, float]:
    """
    对 force、charge1、charge2 和 distance 中任意三个给定值应用库仑定律，
    并在 Python 字典中返回取零参数的名称/数值对。

    库仑定律指出，两个点电荷之间静电吸引力或排斥力的大小与电荷量大小的乘积
    成正比，与两者距离的平方成反比。

    参考资料
    ----------
    Coulomb (1785) "Premier mémoire sur l'électricité et le magnétisme,"
    Histoire de l'Académie Royale des Sciences, pp. 569-577.

    参数
    ----------
    force : float，单位为 Newtons

    charge1 : float，单位为 Coulombs

    charge2 : float，单位为 Coulombs

    distance : float，单位为 meters

    返回值
    -------
    result : dict，取零参数的名称/数值对

    >>> couloumbs_law(force=0, charge1=3, charge2=5, distance=2000)
    {'force': 33705.0}

    >>> couloumbs_law(force=10, charge1=3, charge2=5, distance=0)
    {'distance': 116112.01488218177}

    >>> couloumbs_law(force=10, charge1=0, charge2=5, distance=2000)
    {'charge1': 0.0008900756564307966}

    >>> couloumbs_law(force=0, charge1=0, charge2=5, distance=2000)
    Traceback (most recent call last):
      ...
    ValueError: One and only one argument must be 0

    >>> couloumbs_law(force=0, charge1=3, charge2=5, distance=-2000)
    Traceback (most recent call last):
      ...
    ValueError: Distance cannot be negative

    """

    charge_product = abs(charge1 * charge2)

    if (force, charge1, charge2, distance).count(0) != 1:
        raise ValueError("One and only one argument must be 0")
    if distance < 0:
        raise ValueError("Distance cannot be negative")
    if force == 0:
        force = COULOMBS_CONSTANT * charge_product / (distance**2)
        return {"force": force}
    elif charge1 == 0:
        charge1 = abs(force) * (distance**2) / (COULOMBS_CONSTANT * charge2)
        return {"charge1": charge1}
    elif charge2 == 0:
        charge2 = abs(force) * (distance**2) / (COULOMBS_CONSTANT * charge1)
        return {"charge2": charge2}
    elif distance == 0:
        distance = (COULOMBS_CONSTANT * charge_product / abs(force)) ** 0.5
        return {"distance": distance}
    raise ValueError("Exactly one argument must be 0")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
