"""
标题：计算哈勃参数

说明：哈勃参数 H 表示宇宙在任意时刻的膨胀速率。宇宙学中通常以红移代替
时间，因为远离我们的星系发出的光可直接测得红移。

由此得到一般关系：

H = hubble_constant*(radiation_density*(redshift+1)**4
                     + matter_density*(redshift+1)**3
                     + curvature*(redshift+1)**2 + dark_energy)**(1/2)

其中 radiation_density、matter_density、dark_energy 是当今宇宙中各自的
相对（百分比）能量密度。matter_density 为重子密度与暗物质密度之和。
curvature 是曲率参数，可利用密度完备关系写为：


curvature = 1 - (matter_density + radiation_density + dark_energy)

来源：
https://www.sciencedirect.com/topics/mathematics/hubble-parameter
"""


def hubble_parameter(
    hubble_constant: float,
    radiation_density: float,
    matter_density: float,
    dark_energy: float,
    redshift: float,
) -> float:
    """
    输入参数
    ----------------
    hubble_constant: 哈勃常数，即当前膨胀速率，通常单位为 km/(s*Mpc)

    radiation_density: 当前相对辐射密度

    matter_density: 当前相对物质密度

    dark_energy: 当前相对暗能量密度

    redshift: 光的红移

    返回
    -------
    result : 哈勃参数，单位为 km/s/Mpc（可通过改变哈勃常数的单位来更换单位）

    >>> hubble_parameter(hubble_constant=68.3, radiation_density=1e-4,
    ... matter_density=-0.3, dark_energy=0.7, redshift=1)
    Traceback (most recent call last):
    ...
    ValueError: All input parameters must be positive

    >>> hubble_parameter(hubble_constant=68.3, radiation_density=1e-4,
    ... matter_density= 1.2, dark_energy=0.7, redshift=1)
    Traceback (most recent call last):
    ...
    ValueError: Relative densities cannot be greater than one

    >>> hubble_parameter(hubble_constant=68.3, radiation_density=1e-4,
    ... matter_density= 0.3, dark_energy=0.7, redshift=0)
    68.3
    """
    parameters = [redshift, radiation_density, matter_density, dark_energy]
    if any(p < 0 for p in parameters):
        raise ValueError("All input parameters must be positive")

    if any(p > 1 for p in parameters[1:4]):
        raise ValueError("Relative densities cannot be greater than one")
    curvature = 1 - (matter_density + radiation_density + dark_energy)

    e_2 = (
        radiation_density * (redshift + 1) ** 4
        + matter_density * (redshift + 1) ** 3
        + curvature * (redshift + 1) ** 2
        + dark_energy
    )

    hubble = hubble_constant * e_2 ** (1 / 2)
    return hubble


if __name__ == "__main__":
    import doctest

    # 运行 doctest
    doctest.testmod()

    # 演示 LCDM 近似
    matter_density = 0.3

    print(
        hubble_parameter(
            hubble_constant=68.3,
            radiation_density=1e-4,
            matter_density=matter_density,
            dark_energy=1 - matter_density,
            redshift=0,
        )
    )
