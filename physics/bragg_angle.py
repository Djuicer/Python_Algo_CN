import math


def bragg_angle(distance: float, order: int, wavelength: float) -> float:
    """
    使用以下公式计算布拉格衍射角：
    sin(θ) = (n * λ) / (2 * d)

    参数：
    distance d (float): 晶面间距（单位：米）。
    order n (int): 反射级次。
    wavelength λ (float): 辐射波长（单位：米）。

    示例：
    >>> bragg_angle(2.2e-10, 1, 2.2e-10)
    30.0

    >>> bragg_angle(5e-10, 2, 1e-10)
    11.5

    >>> bragg_angle(4e-10, 1, 4e-10)
    30.0

    # 正弦值无效（超出范围）的测试用例
    >>> bragg_angle(1e-10, 2, 3e-10)
    Traceback (most recent call last):
        ...
    ValueError: The calculated sine value is out of the valid range.
    """
    sine_theta = (order * wavelength) / (2 * distance)
    if sine_theta > 1 or sine_theta < -1:
        raise ValueError("The calculated sine value is out of the valid range.")
    theta_radians = math.asin(sine_theta)
    theta_degrees = math.degrees(theta_radians)
    return round(theta_degrees, 1)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
