"""
根据离散粒子系统中各粒子的位置和质量计算质心。

说明：

在物理学中，空间质量分布的质心（有时称重心或平衡点）是在任意时刻使质量
加权相对位置之和为零的唯一点。对该点施力可产生线加速度而不产生角加速度。

以质心为参考建立力学公式通常能简化计算。质心是假想的质量集中点，便于
描述物体运动。换言之，在应用牛顿运动定律时，质心是给定物体对应的等效粒子。

对于粒子系统 P_i（i = 1, ..., n），各粒子质量为 m_i、空间坐标为 r_i，
其质心坐标 R 为：

R = (Σ(mi * ri) / Σ(mi))

参考资料：https://en.wikipedia.org/wiki/Center_of_mass
"""

from collections import namedtuple

Particle = namedtuple("Particle", "x y z mass")  # noqa: PYI024
Coord3D = namedtuple("Coord3D", "x y z")  # noqa: PYI024


def center_of_mass(particles: list[Particle]) -> Coord3D:
    """
    输入参数
    ----------------
    particles: list(Particle):
    粒子列表，每个粒子是包含其 (x, y, z) 位置和质量的元组。

    返回
    -------
    Coord3D:
    包含质心坐标 (Xcm, Ycm, Zcm) 的元组，保留两位小数。

    示例
    --------
    >>> center_of_mass([
    ...     Particle(1.5, 4, 3.4, 4),
    ...     Particle(5, 6.8, 7, 8.1),
    ...     Particle(9.4, 10.1, 11.6, 12)
    ... ])
    Coord3D(x=6.61, y=7.98, z=8.69)

    >>> center_of_mass([
    ...     Particle(1, 2, 3, 4),
    ...     Particle(5, 6, 7, 8),
    ...     Particle(9, 10, 11, 12)
    ... ])
    Coord3D(x=6.33, y=7.33, z=8.33)

    >>> center_of_mass([
    ...     Particle(1, 2, 3, -4),
    ...     Particle(5, 6, 7, 8),
    ...     Particle(9, 10, 11, 12)
    ... ])
    Traceback (most recent call last):
        ...
    ValueError: Mass of all particles must be greater than 0

    >>> center_of_mass([
    ...     Particle(1, 2, 3, 0),
    ...     Particle(5, 6, 7, 8),
    ...     Particle(9, 10, 11, 12)
    ... ])
    Traceback (most recent call last):
        ...
    ValueError: Mass of all particles must be greater than 0

    >>> center_of_mass([])
    Traceback (most recent call last):
        ...
    ValueError: No particles provided
    """
    if not particles:
        raise ValueError("No particles provided")

    if any(particle.mass <= 0 for particle in particles):
        raise ValueError("Mass of all particles must be greater than 0")

    total_mass = sum(particle.mass for particle in particles)

    center_of_mass_x = round(
        sum(particle.x * particle.mass for particle in particles) / total_mass, 2
    )
    center_of_mass_y = round(
        sum(particle.y * particle.mass for particle in particles) / total_mass, 2
    )
    center_of_mass_z = round(
        sum(particle.z * particle.mass for particle in particles) / total_mass, 2
    )
    return Coord3D(center_of_mass_x, center_of_mass_y, center_of_mass_z)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
