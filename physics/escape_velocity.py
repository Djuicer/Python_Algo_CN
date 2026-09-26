import math


def escape_velocity(mass: float, radius: float) -> float:
    """
    计算脱离天体引力场所需的逃逸速度。

    使用公式：
        v = sqrt(2 * G * M / R)

    其中：
        v = 逃逸速度 (m/s)
        G = 引力常数 (6.67430 * 10^-11 m^3 kg^-1 s^-2)
        M = 天体质量 (kg)
        R = 到质心的距离 (m)

    来源：
        https://en.wikipedia.org/wiki/Escape_velocity

    参数：
        mass (float): 天体质量，单位为千克。
        radius (float): 到质心的距离，单位为米。

    返回：
        float: 逃逸速度，单位为米每秒，保留 3 位小数。

    示例：
        >>> escape_velocity(mass=5.972e24, radius=6.371e6)  # Earth
        11185.978
        >>> escape_velocity(mass=7.348e22, radius=1.737e6)  # Moon
        2376.307
        >>> escape_velocity(mass=1.898e27, radius=6.9911e7)  # Jupiter
        60199.545
        >>> escape_velocity(mass=0, radius=1.0)
        0.0
        >>> escape_velocity(mass=1.0, radius=0)
        Traceback (most recent call last):
            ...
        ZeroDivisionError: Radius cannot be zero.
    """
    gravitational_constant = 6.67430e-11  # m^3 kg^-1 s^-2

    if radius == 0:
        raise ZeroDivisionError("Radius cannot be zero.")

    velocity = math.sqrt(2 * gravitational_constant * mass / radius)
    return round(velocity, 3)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Calculate escape velocity of a celestial body...\n")

    try:
        mass = float(input("Enter mass of the celestial body (in kgs): ").strip())
        radius = float(input("Enter radius from the center of mass (in ms): ").strip())

        velocity = escape_velocity(mass=mass, radius=radius)
        print(f"Escape velocity is {velocity} m/s")

    except ValueError:
        print("Invalid input. Please enter valid numeric values.")
    except ZeroDivisionError as e:
        print(e)
