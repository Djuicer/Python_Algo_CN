"""
均方根速率是衡量气体中粒子平均速率的重要指标，定义为：
 -----------------
 | Vrms = √3RT/M |
 -----------------

在气体分子运动论中，气体粒子持续进行随机运动；各粒子的速率不同，不断
碰撞并改变方向。速度同时考虑速率与方向，用于描述气体粒子的运动。尽管
各粒子的速度不断变化，速度分布却保持不变。我们无法测量每个粒子的速度，
因此通常研究粒子的平均行为。相反方向的速度符号相反；由于气体粒子随机
运动，各方向上的粒子数量大致相同，所以粒子集合的平均速度为零。这个值
意义有限，因此可使用另一种方法确定平均速率。
"""

UNIVERSAL_GAS_CONSTANT = 8.3144598


def rms_speed_of_molecule(temperature: float, molar_mass: float) -> float:
    """
    >>> rms_speed_of_molecule(100, 2)
    35.315279554323226
    >>> rms_speed_of_molecule(273, 12)
    23.821458421977443
    """
    if temperature < 0:
        raise Exception("Temperature cannot be less than 0 K")
    if molar_mass <= 0:
        raise Exception("Molar mass cannot be less than or equal to 0 kg/mol")
    return (3 * UNIVERSAL_GAS_CONSTANT * temperature / molar_mass) ** 0.5


if __name__ == "__main__":
    import doctest

    # 运行 doctest
    doctest.testmod()

    # 示例
    temperature = 300
    molar_mass = 28
    vrms = rms_speed_of_molecule(temperature, molar_mass)
    print(f"Vrms of Nitrogen gas at 300 K is {vrms} m/s")
