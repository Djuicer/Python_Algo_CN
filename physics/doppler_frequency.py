"""
多普勒效应

多普勒效应（又称多普勒频移）是观察者相对于波源运动时所观测到的波频率变化，
以物理学家 Christian Doppler 命名。常见示例是鸣笛车辆接近和远离观察者时，
听到的音调发生变化。

当波源向观察者移动时，后一个波峰的发射位置比前一个更接近观察者，因此
到达观察者所需时间略短，相邻波峰的到达时间间隔缩短，频率升高。类似地，
波源远离观察者时，后续波从更远的位置发出，到达间隔增大，频率降低。

若波源静止而观察者相对波源运动，即使波源发出的波长和频率不变，观察者接收
波的速率也会改变。

这些结果可由多普勒公式概括：

    f = (f0 * (v + v0)) / (v - vs)

其中：
    f: 波的频率
    f0: 波源静止时的波频率
    v: 波在介质中的传播速度
    v0: 观察者速度，向波源运动时为正
    vs: 波源速度，向观察者运动时为正

多普勒效应在物理和工程中应用广泛，例如雷达、天文学、医学成像和地震学。

参考资料：
https://en.wikipedia.org/wiki/Doppler_effect

下面实现一个函数，根据波源静止时的频率、波在介质中的速度、观察者速度和
波源速度计算观测频率。
"""


def doppler_effect(
    org_freq: float, wave_vel: float, obs_vel: float, src_vel: float
) -> float:
    """
    输入参数：
    -----------------
    org_freq: 波源静止时的波频率
    wave_vel: 波在介质中的传播速度
    obs_vel: 观察者速度，向波源运动时为正
    src_vel: 波源速度，向观察者运动时为正

    返回：
    --------
    f: 观察者感知到的波频率

    Docstring 测试：
    >>> doppler_effect(100, 330, 10, 0)  # observer moving towards the source
    103.03030303030303
    >>> doppler_effect(100, 330, -10, 0)  # observer moving away from the source
    96.96969696969697
    >>> doppler_effect(100, 330, 0, 10)  # source moving towards the observer
    103.125
    >>> doppler_effect(100, 330, 0, -10)  # source moving away from the observer
    97.05882352941177
    >>> doppler_effect(100, 330, 10, 10)  # source & observer moving towards each other
    106.25
    >>> doppler_effect(100, 330, -10, -10)  # source and observer moving away
    94.11764705882354
    >>> doppler_effect(100, 330, 10, 330)  # source moving at same speed as the wave
    Traceback (most recent call last):
        ...
    ZeroDivisionError: Division by zero implies vs=v and observer in front of the source
    >>> doppler_effect(100, 330, 10, 340)  # source moving faster than the wave
    Traceback (most recent call last):
        ...
    ValueError: Non-positive frequency implies vs>v or v0>v (in the opposite direction)
    >>> doppler_effect(100, 330, -340, 10)  # observer moving faster than the wave
    Traceback (most recent call last):
        ...
    ValueError: Non-positive frequency implies vs>v or v0>v (in the opposite direction)
    """

    if wave_vel == src_vel:
        raise ZeroDivisionError(
            "Division by zero implies vs=v and observer in front of the source"
        )
    doppler_freq = (org_freq * (wave_vel + obs_vel)) / (wave_vel - src_vel)
    if doppler_freq <= 0:
        raise ValueError(
            "Non-positive frequency implies vs>v or v0>v (in the opposite direction)"
        )
    return doppler_freq


if __name__ == "__main__":
    import doctest

    doctest.testmod()
