"""
在物理学和天文学中，引力 N 体模拟用于模拟粒子在引力影响下组成的动力系统。
系统包含若干天体，每个天体都对其他天体施加引力，这些力依据牛顿万有引力
定律计算。每个时间步使用 Euler 法计算这些力引起的速度和位置变化。当一个
粒子过于接近另一个粒子（使力趋于无穷大）时，使用软化技术防止数值发散。
（说明改编自 https://en.wikipedia.org/wiki/N-body_simulation ）
（另见 http://www.shodor.org/refdesk/Resources/Algorithms/EulersMethod/ ）
"""

from __future__ import annotations

import random

from matplotlib import animation
from matplotlib import pyplot as plt

# 动画帧率
INTERVAL = 20

# 时间步之间的间隔，单位为秒
DELTA_TIME = INTERVAL / 1000


class Body:
    def __init__(
        self,
        position_x: float,
        position_y: float,
        velocity_x: float,
        velocity_y: float,
        mass: float = 1.0,
        size: float = 1.0,
        color: str = "blue",
    ) -> None:
        """
        参数 "size" 和 "color" 与模拟本身无关，仅用于绘图。
        """
        self.position_x = position_x
        self.position_y = position_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.mass = mass
        self.size = size
        self.color = color

    @property
    def position(self) -> tuple[float, float]:
        return self.position_x, self.position_y

    @property
    def velocity(self) -> tuple[float, float]:
        return self.velocity_x, self.velocity_y

    def update_velocity(
        self, force_x: float, force_y: float, delta_time: float
    ) -> None:
        """
        用于更新速度的 Euler 算法。

        >>> body_1 = Body(0.,0.,0.,0.)
        >>> body_1.update_velocity(1.,0.,1.)
        >>> body_1.velocity
        (1.0, 0.0)

        >>> body_1.update_velocity(1.,0.,1.)
        >>> body_1.velocity
        (2.0, 0.0)

        >>> body_2 = Body(0.,0.,5.,0.)
        >>> body_2.update_velocity(0.,-10.,10.)
        >>> body_2.velocity
        (5.0, -100.0)

        >>> body_2.update_velocity(0.,-10.,10.)
        >>> body_2.velocity
        (5.0, -200.0)
        """
        self.velocity_x += force_x * delta_time
        self.velocity_y += force_y * delta_time

    def update_position(self, delta_time: float) -> None:
        """
        用于更新位置的 Euler 算法。

        >>> body_1 = Body(0.,0.,1.,0.)
        >>> body_1.update_position(1.)
        >>> body_1.position
        (1.0, 0.0)

        >>> body_1.update_position(1.)
        >>> body_1.position
        (2.0, 0.0)

        >>> body_2 = Body(10.,10.,0.,-2.)
        >>> body_2.update_position(1.)
        >>> body_2.position
        (10.0, 8.0)

        >>> body_2.update_position(1.)
        >>> body_2.position
        (10.0, 6.0)
        """
        self.position_x += self.velocity_x * delta_time
        self.position_y += self.velocity_y * delta_time


class BodySystem:
    """
    本类用于保存天体、引力常数、时间因子和软化因子。时间因子用于控制模拟
    速度。软化因子用于软化，这是 N 体模拟中防止两个天体距离过近时发生
    数值发散的技巧。
    """

    def __init__(
        self,
        bodies: list[Body],
        gravitation_constant: float = 1.0,
        time_factor: float = 1.0,
        softening_factor: float = 0.0,
    ) -> None:
        self.bodies = bodies
        self.gravitation_constant = gravitation_constant
        self.time_factor = time_factor
        self.softening_factor = softening_factor

    def __len__(self) -> int:
        return len(self.bodies)

    def update_system(self, delta_time: float) -> None:
        """
        对每个天体遍历其他所有天体，计算它们对该天体施加的合力，并用此力
        更新天体速度。

        >>> body_system_1 = BodySystem([Body(0,0,0,0), Body(10,0,0,0)])
        >>> len(body_system_1)
        2
        >>> body_system_1.update_system(1)
        >>> body_system_1.bodies[0].position
        (0.01, 0.0)
        >>> body_system_1.bodies[0].velocity
        (0.01, 0.0)

        >>> body_system_2 = BodySystem([Body(-10,0,0,0), Body(10,0,0,0, mass=4)], 1, 10)
        >>> body_system_2.update_system(1)
        >>> body_system_2.bodies[0].position
        (-9.0, 0.0)
        >>> body_system_2.bodies[0].velocity
        (0.1, 0.0)
        """
        for body1 in self.bodies:
            force_x = 0.0
            force_y = 0.0
            for body2 in self.bodies:
                if body1 != body2:
                    dif_x = body2.position_x - body1.position_x
                    dif_y = body2.position_y - body1.position_y

                    # 使用勾股定理计算距离
                    # 软化技术引入的额外因子
                    distance = (dif_x**2 + dif_y**2 + self.softening_factor) ** (1 / 2)

                    # 牛顿万有引力定律
                    force_x += (
                        self.gravitation_constant * body2.mass * dif_x / distance**3
                    )
                    force_y += (
                        self.gravitation_constant * body2.mass * dif_y / distance**3
                    )

            # 累加所有力分量后更新天体速度
            body1.update_velocity(force_x, force_y, delta_time * self.time_factor)

        # 仅在所有速度更新后再更新位置
        for body in self.bodies:
            body.update_position(delta_time * self.time_factor)


def update_step(
    body_system: BodySystem, delta_time: float, patches: list[plt.Circle]
) -> None:
    """
    更新天体系统，并将变化应用到绘图使用的图形块列表。

    >>> body_system_1 = BodySystem([Body(0,0,0,0), Body(10,0,0,0)])
    >>> patches_1 = [plt.Circle((body.position_x, body.position_y), body.size,
    ... fc=body.color)for body in body_system_1.bodies] #doctest: +ELLIPSIS
    >>> update_step(body_system_1, 1, patches_1)
    >>> patches_1[0].center
    (0.01, 0.0)

    >>> body_system_2 = BodySystem([Body(-10,0,0,0), Body(10,0,0,0, mass=4)], 1, 10)
    >>> patches_2 = [plt.Circle((body.position_x, body.position_y), body.size,
    ... fc=body.color)for body in body_system_2.bodies] #doctest: +ELLIPSIS
    >>> update_step(body_system_2, 1, patches_2)
    >>> patches_2[0].center
    (-9.0, 0.0)
    """
    # 更新天体位置
    body_system.update_system(delta_time)

    # 更新图形块位置
    for patch, body in zip(patches, body_system.bodies):
        patch.center = (body.position_x, body.position_y)


def plot(
    title: str,
    body_system: BodySystem,
    x_start: float = -1,
    x_end: float = 1,
    y_start: float = -1,
    y_end: float = 1,
) -> None:
    """
    绘制给定天体系统随时间演化过程的工具函数。
    本函数没有返回值，因此未提供 doctest。
    """
    fig = plt.figure()
    fig.canvas.manager.set_window_title(title)
    ax = plt.axes(
        xlim=(x_start, x_end), ylim=(y_start, y_end)
    )  # 设置绘图区域
    plt.gca().set_aspect("equal")  # 固定纵横比

    # plt 函数将每个天体绘制为一个图形块
    patches = [
        plt.Circle((body.position_x, body.position_y), body.size, fc=body.color)
        for body in body_system.bodies
    ]

    for patch in patches:
        ax.add_patch(patch)

    # 动画每一步调用的函数
    def update(frame: int) -> list[plt.Circle]:  # noqa: ARG001
        update_step(body_system, DELTA_TIME, patches)
        return patches

    anim = animation.FuncAnimation(  # noqa: F841
        fig, update, interval=INTERVAL, blit=True
    )

    plt.show()


def example_1() -> BodySystem:
    """
    示例 1：三体问题的 8 字形解。
    此示例可视为对实现的测试：给定正确初始条件，天体应沿 8 字形运动。
    （初始条件取自 http://www.artcompsci.org/vol_1/v1_web/node56.html）
    >>> body_system = example_1()
    >>> len(body_system)
    3
    """

    position_x = 0.9700436
    position_y = -0.24308753
    velocity_x = 0.466203685
    velocity_y = 0.43236573

    bodies1 = [
        Body(position_x, position_y, velocity_x, velocity_y, size=0.2, color="red"),
        Body(-position_x, -position_y, velocity_x, velocity_y, size=0.2, color="green"),
        Body(0, 0, -2 * velocity_x, -2 * velocity_y, size=0.2, color="blue"),
    ]
    return BodySystem(bodies1, time_factor=3)


def example_2() -> BodySystem:
    """
    示例 2：月球绕地球运行的轨道。
    此示例可视为对实现的测试：给定正确初始条件，月球应像实际情况一样绕
    地球运行。（质量、速度和距离取自 https://en.wikipedia.org/wiki/Earth
    和 https://en.wikipedia.org/wiki/Moon）
    本函数没有返回值，因此未提供 doctest。
    """

    moon_mass = 7.3476e22
    earth_mass = 5.972e24
    velocity_dif = 1022
    earth_moon_distance = 384399000
    gravitation_constant = 6.674e-11

    # 计算各自的速度，使总动量为零，即两个天体整体不移动
    moon_velocity = earth_mass * velocity_dif / (earth_mass + moon_mass)
    earth_velocity = moon_velocity - velocity_dif

    moon = Body(-earth_moon_distance, 0, 0, moon_velocity, moon_mass, 10000000, "grey")
    earth = Body(0, 0, 0, earth_velocity, earth_mass, 50000000, "blue")
    return BodySystem([earth, moon], gravitation_constant, time_factor=1000000)


def example_3() -> BodySystem:
    """
    示例 3：包含多个天体的随机系统。
    本函数没有返回值，因此未提供 doctest。
    """

    bodies = []
    for _ in range(10):
        velocity_x = random.uniform(-0.5, 0.5)
        velocity_y = random.uniform(-0.5, 0.5)

        # 成对创建速度相反的天体，使总动量保持为零
        bodies.append(
            Body(
                random.uniform(-0.5, 0.5),
                random.uniform(-0.5, 0.5),
                velocity_x,
                velocity_y,
                size=0.05,
            )
        )
        bodies.append(
            Body(
                random.uniform(-0.5, 0.5),
                random.uniform(-0.5, 0.5),
                -velocity_x,
                -velocity_y,
                size=0.05,
            )
        )
    return BodySystem(bodies, 0.01, 10, 0.1)


if __name__ == "__main__":
    plot("Figure-8 solution to the 3-body-problem", example_1(), -2, 2, -2, 2)
    plot(
        "Moon's orbit around the earth",
        example_2(),
        -430000000,
        430000000,
        -430000000,
        430000000,
    )
    plot("Random system with many bodies", example_3(), -1.5, 1.5, -1.5, 1.5)
