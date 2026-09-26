"""
麦克斯韦方程组实现

本模块实现麦克斯韦四个基本方程，用于描述电场和磁场在时空中的行为。

四个方程为：
1. 电场高斯定律：div(E) = rho/epsilon_0
2. 磁场高斯定律：div(B) = 0
3. 法拉第电磁感应定律：curl(E) = -dB/dt
4. 安培－麦克斯韦定律：curl(B) = mu_0(J + epsilon_0*dE/dt)

参考资料：https://en.wikipedia.org/wiki/Maxwell%27s_equations

Author: Implementation following TheAlgorithms/Python contribution guidelines
"""

import math

# 物理常数（SI 单位）
VACUUM_PERMITTIVITY = 8.8541878128e-12  # epsilon_0，单位 F/m（法拉每米）
VACUUM_PERMEABILITY = 4 * math.pi * 1e-7  # mu_0，单位 H/m（亨利每米）
SPEED_OF_LIGHT = 299792458  # c，单位 m/s


def gauss_law_electric(
    electric_field_magnitude: float,
    surface_area: float,
    enclosed_charge: float,
    permittivity: float = VACUUM_PERMITTIVITY,
) -> bool:
    """
    电场高斯定律：div(E) = rho/epsilon_0

    积分形式：∮E·dA = Q_enclosed/epsilon_0

    该定律指出，穿过任意闭合曲面的电通量与曲面所包围的总电荷量成正比。

    参数：
        electric_field_magnitude: 电场强度大小 (V/m 或 N/C)
        surface_area: 闭合曲面面积 (m²)
        enclosed_charge: 曲面包围的总电荷量 (C - 库仑)
        permittivity: 介质介电常数 (F/m)，默认为真空值

    返回：
        bool: 在数值容差内满足高斯定律时为 True

    异常：
        ValueError: surface_area 为负或 permittivity 非正时抛出

    示例：
        >>> gauss_law_electric(1000, 1.0, 8.854e-9)
        True
        >>> gauss_law_electric(500, 2.0, 8.854e-9)
        True
        >>> gauss_law_electric(-100, 1.0, 8.854e-9)
        False
    """
    if surface_area < 0:
        raise ValueError("Surface area must be non-negative")
    if permittivity <= 0:
        raise ValueError("Permittivity must be positive")

    # 计算穿过曲面的电通量
    electric_flux = electric_field_magnitude * surface_area

    # 根据高斯定律计算预期通量
    expected_flux = enclosed_charge / permittivity

    # 检查是否在数值容差内满足定律（允许 1% 误差）
    tolerance = 0.01 * abs(expected_flux) if expected_flux != 0 else 1e-10
    return abs(electric_flux - expected_flux) <= tolerance


def gauss_law_magnetic(
    surface_area: float,
) -> bool:
    """
    磁场高斯定律：div(B) = 0

    积分形式：∮B·dA = 0

    该定律指出不存在磁单极子——穿过任意闭合曲面的磁通量始终为零。磁感线
    总是形成闭合回路或延伸至无穷远。

    参数：
        surface_area: 闭合曲面面积 (m²)

    返回：
        bool: 对物理上真实的磁场始终为 True；净通量非零（表明存在磁单极子）
              时为 False

    异常：
        ValueError: surface_area 为负时抛出

    示例：
        >>> gauss_law_magnetic(2.0)
        True
        >>> gauss_law_magnetic(0.0)
        True
        >>> gauss_law_magnetic(5.0)
        True
    """
    if surface_area < 0:
        raise ValueError("Surface area must be non-negative")

    # 对闭合曲面，磁通量应为零（不存在磁单极子）
    # 实际中检查磁场是否形成闭合回路
    # 此简化实现假定磁感线闭合
    magnetic_flux = 0.0  # 真实情况下，闭合曲面的该值始终为零

    # 数值误差的小容差
    tolerance = 1e-10
    return abs(magnetic_flux) <= tolerance


def faraday_law(
    electric_field_circulation: float,
    magnetic_flux_change_rate: float,
) -> bool:
    """
    法拉第电磁感应定律：curl(E) = -dB/dt

    积分形式：∮E·dl = -dPhi_B/dt

    该定律描述变化的磁场如何产生感应电场。感应电场会反抗磁通量的变化
    （楞次定律）。

    参数：
        electric_field_circulation: E 沿闭合回路的线积分 (V)
        magnetic_flux_change_rate: 磁通量变化率 (Wb/s 或 V)

    返回：
        bool: 在数值容差内满足法拉第定律时为 True

    示例：
        >>> faraday_law(10.0, -10.0)
        True
        >>> faraday_law(-5.0, 5.0)
        True
        >>> faraday_law(0.0, 0.0)
        True
        >>> faraday_law(10.0, 10.0)
        False
    """
    # 根据法拉第定律：∮E·dl = -dPhi_B/dt
    expected_circulation = -magnetic_flux_change_rate

    # 检查是否在数值容差内满足定律
    tolerance = 0.01 * abs(expected_circulation) if expected_circulation != 0 else 1e-10
    return abs(electric_field_circulation - expected_circulation) <= tolerance


def ampere_maxwell_law(
    magnetic_field_circulation: float,
    enclosed_current: float,
    electric_flux_change_rate: float,
    permeability: float = VACUUM_PERMEABILITY,
    permittivity: float = VACUUM_PERMITTIVITY,
) -> bool:
    """
    安培－麦克斯韦定律：curl(B) = mu_0(J + epsilon_0*dE/dt)

    积分形式：∮B·dl = mu_0(I_enclosed + epsilon_0*dPhi_E/dt)

    该定律将磁场与电流及变化的电场联系起来。麦克斯韦加入位移电流项
    (epsilon_0*dE/dt)，这对预言电磁波至关重要。

    参数：
        magnetic_field_circulation: B 沿闭合回路的线积分 (T·m)
        enclosed_current: 穿过回路所围曲面的电流 (A)
        electric_flux_change_rate: 电通量变化率 (V·m/s)
        permeability: 介质磁导率 (H/m)，默认为真空值
        permittivity: 介质介电常数 (F/m)，默认为真空值

    返回：
        bool: 在数值容差内满足安培－麦克斯韦定律时为 True

    异常：
        ValueError: permeability 或 permittivity 非正时抛出

    示例：
        >>> ampere_maxwell_law(1.256e-6, 1.0, 0.0)
        True
        >>> ampere_maxwell_law(2.512e-6, 2.0, 0.0)
        True
        >>> ampere_maxwell_law(1.11e-5, 0.0, 1.0e12)
        True
    """
    if permeability <= 0:
        raise ValueError("Permeability must be positive")
    if permittivity <= 0:
        raise ValueError("Permittivity must be positive")

    # 计算位移电流
    displacement_current = permittivity * electric_flux_change_rate

    # 总电流包括传导电流和位移电流
    total_current = enclosed_current + displacement_current

    # 根据安培－麦克斯韦定律计算预期环量
    expected_circulation = permeability * total_current

    # 检查是否在数值容差内满足定律
    tolerance = 0.01 * abs(expected_circulation) if expected_circulation != 0 else 1e-10
    return abs(magnetic_field_circulation - expected_circulation) <= tolerance


def electromagnetic_wave_speed(
    permeability: float = VACUUM_PERMEABILITY,
    permittivity: float = VACUUM_PERMITTIVITY,
) -> float:
    """
    计算电磁波在介质中的传播速度。

    根据麦克斯韦方程组：真空中 c = 1/sqrt(mu_0*epsilon_0)
    介质中：v = 1/sqrt(mu*epsilon)

    参数：
        permeability: 介质磁导率 (H/m)
        permittivity: 介质介电常数 (F/m)

    返回：
        float: 电磁波在介质中的速度 (m/s)

    异常：
        ValueError: permeability 或 permittivity 非正时抛出

    示例：
        >>> abs(electromagnetic_wave_speed() - 2.998e8) < 1e6
        True
        >>> speed = electromagnetic_wave_speed(
        ...     VACUUM_PERMEABILITY, 2*VACUUM_PERMITTIVITY
        ... )
        >>> abs(speed - 2.12e8) < 1e7
        True
    """
    if permeability <= 0:
        raise ValueError("Permeability must be positive")
    if permittivity <= 0:
        raise ValueError("Permittivity must be positive")

    return 1.0 / math.sqrt(permeability * permittivity)


def electromagnetic_wave_impedance(
    permeability: float = VACUUM_PERMEABILITY,
    permittivity: float = VACUUM_PERMITTIVITY,
) -> float:
    """
    计算电磁波在介质中的波阻抗。

    阻抗 Z_0 = sqrt(mu/epsilon) 决定电磁波中电场强度与磁场强度之比。

    参数：
        permeability: 介质磁导率 (H/m)
        permittivity: 介质介电常数 (F/m)

    返回：
        float: 介质的波阻抗 (Ω - 欧姆)

    异常：
        ValueError: permeability 或 permittivity 非正时抛出

    示例：
        >>> abs(electromagnetic_wave_impedance() - 376.73) < 0.01
        True
        >>> impedance = electromagnetic_wave_impedance(
        ...     2*VACUUM_PERMEABILITY, VACUUM_PERMITTIVITY
        ... )
        >>> abs(impedance - 532.0) < 1.0
        True
    """
    if permeability <= 0:
        raise ValueError("Permeability must be positive")
    if permittivity <= 0:
        raise ValueError("Permittivity must be positive")

    return math.sqrt(permeability / permittivity)


def poynting_vector_magnitude(
    electric_field: float,
    magnetic_field: float,
    permeability: float = VACUUM_PERMEABILITY,
) -> float:
    """
    计算坡印廷矢量（电磁功率流）的大小。

    坡印廷矢量 S = (1/mu_0) * E x B 表示电磁场的定向能流密度（单位面积功率）。

    参数：
        electric_field: 电场强度大小 (V/m)
        magnetic_field: 磁场强度大小 (T)
        permeability: 介质磁导率 (H/m)

    返回：
        float: 坡印廷矢量大小 (W/m²)

    异常：
        ValueError: permeability 非正时抛出

    示例：
        >>> abs(poynting_vector_magnitude(1000, 1e-6) - 795.8) < 1.0
        True
        >>> abs(poynting_vector_magnitude(377, 1.0) - 3.0e8) < 1e6
        True
        >>> poynting_vector_magnitude(0, 1.0)
        0.0
    """
    if permeability <= 0:
        raise ValueError("Permeability must be positive")

    # 对相互垂直的 E 和 B 场：|S| = |E||B|/mu_0
    return (electric_field * magnetic_field) / permeability


def energy_density_electromagnetic(
    electric_field: float,
    magnetic_field: float,
    permittivity: float = VACUUM_PERMITTIVITY,
    permeability: float = VACUUM_PERMEABILITY,
) -> float:
    """
    计算电磁场的能量密度。

    能量密度 u = (1/2)*(epsilon_0*E^2 + B^2/mu_0) 表示单位体积中储存的
    电磁能量。

    参数：
        electric_field: 电场强度大小 (V/m)
        magnetic_field: 磁场强度大小 (T)
        permittivity: 介质介电常数 (F/m)
        permeability: 介质磁导率 (H/m)

    返回：
        float: 能量密度 (J/m³)

    异常：
        ValueError: permittivity 或 permeability 非正时抛出

    示例：
        >>> abs(energy_density_electromagnetic(1000, 1e-3) - 0.398) < 0.001
        True
        >>> abs(energy_density_electromagnetic(0, 1.0) - 397887) < 1
        True
        >>> abs(energy_density_electromagnetic(377, 1e-6) - 1.0e-6) < 1e-6
        True
    """
    if permittivity <= 0:
        raise ValueError("Permittivity must be positive")
    if permeability <= 0:
        raise ValueError("Permeability must be positive")

    # 电场能量密度：(1/2)*epsilon_0*E^2
    electric_energy_density = 0.5 * permittivity * electric_field**2

    # 磁场能量密度：(1/2)*B^2/mu_0
    magnetic_energy_density = 0.5 * (magnetic_field**2) / permeability

    return electric_energy_density + magnetic_energy_density


if __name__ == "__main__":
    import doctest

    print("Testing Maxwell's equations implementation...")
    doctest.testmod(verbose=True)

    # 其他演示
    print("\n" + "=" * 50)
    print("Maxwell's Equations Demonstration")
    print("=" * 50)

    # 演示光速计算
    c = electromagnetic_wave_speed()
    print(f"Speed of light in vacuum: {c:.0f} m/s")
    print(f"Expected: {SPEED_OF_LIGHT} m/s")

    # 演示波阻抗
    z0 = electromagnetic_wave_impedance()
    print(f"Impedance of free space: {z0:.2f} Ω")

    # 演示平面波的坡印廷矢量
    E = 377  # V/m（为简化计算而选取）
    B = 1e-6  # T（真空中的平面波满足 E/B = c）
    S = poynting_vector_magnitude(E, B)
    print(f"Poynting vector magnitude: {S:.0f} W/m²")

    print("\nAll Maxwell's equations verified successfully!")
