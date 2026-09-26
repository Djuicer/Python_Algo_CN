"""
相对论速度叠加公式用于计算合速度 v2：物体相对于某参考系以速度 v1 运动，
而该参考系相对于观察者以速度 v 运动。这里假定后者严格小于光速。
公式为 v2 = (v1 + v)/(1 + v1 * v / c**2)
v1 - 物体相对于运动参考系的速度
v - 运动参考系的速度
c - 真空中的光速
v2 - 物体相对于观察者的速度

https://en.wikipedia.org/wiki/Velocity-addition_formula
"""

c = 299792458


def relativistic_velocity_summation(
    object_velocity: float, frame_velocity: float
) -> float:
    """
    >>> relativistic_velocity_summation(200000000, 200000000)
    276805111.0636436
    >>> relativistic_velocity_summation(299792458, 100000000)
    299792458.0
    >>> relativistic_velocity_summation(100000000, 299792458)
    Traceback (most recent call last):
        ...
    ValueError: Speeds must not exceed light speed...
    """
    if (
        object_velocity > c
        or frame_velocity >= c
        or object_velocity < -c
        or frame_velocity <= -c
    ):
        raise ValueError(
            "Speeds must not exceed light speed, and "
            "the frame speed must be lower than the light speed!"
        )
    numerator = object_velocity + frame_velocity
    denominator = 1 + object_velocity * frame_velocity / c**2
    return numerator / denominator


if __name__ == "__main__":
    from doctest import testmod

    testmod()
