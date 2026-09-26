"""
这两个函数返回质量为 M、半径为 R 的目标物体的碰撞半径，以及其有效截面积
sigma。也就是说，以速度 v 进入 sigma 范围内的任意抛射体都会撞击质量为 M
的目标物体。推导过程见文件末尾。

推导表明，由于 R_capture>R_target，抛射体无需直接瞄准目标也能撞击目标。
天文学家将捕获的有效截面积称为 sigma=π*R_capture**2。

本算法不考虑 N 体问题。
"""

from math import pow, sqrt  # noqa: A004

from scipy.constants import G, c, pi


def capture_radii(
    target_body_radius: float, target_body_mass: float, projectile_velocity: float
) -> float:
    """
    输入参数：
    -------------
    target_body_radius: 中心天体半径，SI 单位：米 | m
    target_body_mass: 中心天体质量，SI 单位：千克 | kg
    projectile_velocity: 向中心天体运动的物体速度，SI 单位：米/秒 | m/s
    返回：
    --------
    >>> capture_radii(6.957e8, 1.99e30, 25000.0)
    17209590691.0
    >>> capture_radii(-6.957e8, 1.99e30, 25000.0)
    Traceback (most recent call last):
        ...
    ValueError: Radius cannot be less than 0
    >>> capture_radii(6.957e8, -1.99e30, 25000.0)
    Traceback (most recent call last):
        ...
    ValueError: Mass cannot be less than 0
    >>> capture_radii(6.957e8, 1.99e30, c+1)
    Traceback (most recent call last):
        ...
    ValueError: Cannot go beyond speed of light

    返回值的 SI 单位：
    ------------------
    meters | m
    """

    if target_body_mass < 0:
        raise ValueError("Mass cannot be less than 0")
    if target_body_radius < 0:
        raise ValueError("Radius cannot be less than 0")
    if projectile_velocity > c:
        raise ValueError("Cannot go beyond speed of light")

    escape_velocity_squared = (2 * G * target_body_mass) / target_body_radius
    capture_radius = target_body_radius * sqrt(
        1 + escape_velocity_squared / pow(projectile_velocity, 2)
    )
    return round(capture_radius, 0)


def capture_area(capture_radius: float) -> float:
    """
    输入参数：
    ------------
    capture_radius: 对质量为 M 的中心天体及以速度 v 向其运动的抛射体，轨道
    捕获和撞击的半径，SI 单位：米 | m
    返回：
    --------
    >>> capture_area(17209590691)
    9.304455331329126e+20
    >>> capture_area(-1)
    Traceback (most recent call last):
        ...
    ValueError: Cannot have a capture radius less than 0

    返回值的 SI 单位：
    ------------------
    meters*meters | m**2
    """

    if capture_radius < 0:
        raise ValueError("Cannot have a capture radius less than 0")
    sigma = pi * pow(capture_radius, 2)
    return round(sigma, 0)


if __name__ == "__main__":
    from doctest import testmod

    testmod()

"""
推导：

设：Mt=目标质量，Rt=目标半径，v=projectile_velocity，
    r_0=时刻 0 抛射体到目标质心的距离，
    v_p=最接近时的速度 v，
    r_p=最接近时抛射体到目标质心的距离，
    R_capture=速度为 v 的抛射体的碰撞半径

(1) time=0 时，抛射体从无穷远落下的能量 | E=K+U=0.5*m*(v**2)+0

    E_initial=0.5*m*(v**2)

(2) time=0 时，抛射体相对于目标质心的角动量 |
    L_initial=m*r_0*v*sin(Θ)->m*r_0*v*(R_capture/r_0)->m*v*R_capture

    L_i=m*v*R_capture

(3) 抛射体最接近时的能量为此时的动能加引力势能 (-(GMm)/R) |
    E_p=K_p+U_p->E_p=0.5*m*(v_p**2)-(G*Mt*m)/r_p

    E_p=0.0.5*m*(v_p**2)-(G*Mt*m)/r_p

(4)抛射体相对于目标在最接近位置的角动量为
   L_p=m*r_p*v_p*sin(Θ)，但相对于目标，Θ=90°
   sin(90°)=1|

    L_p=m*r_p*v_p
(5) 利用角动量守恒和能量守恒，可写出求解 r_p 的二次方程 |

   (a)
    Ei=Ep-> 0.5*m*(v**2)=0.5*m*(v_p**2)-(G*Mt*m)/r_p-> v**2=v_p**2-(2*G*Mt)/r_p

   (b)
    Li=Lp-> m*v*R_capture=m*r_p*v_p-> v*R_capture=r_p*v_p-> v_p=(v*R_capture)/r_p

   (c) 将 b 代入 a |
    v**2=((v*R_capture)/r_p)**2-(2*G*Mt)/r_p->

    v**2-(v**2)*(R_c**2)/(r_p**2)+(2*G*Mt)/r_p=0->

    (v**2)*(r_p**2)+2*G*Mt*r_p-(v**2)*(R_c**2)=0

   (d) 使用二次方程公式求出 r_p，再整理求出 R_capture

    r_p=(-2*G*Mt ± sqrt(4*G^2*Mt^2+ 4(v^4*R_c^2)))/(2*v^2)->

    r_p=(-G*Mt ± sqrt(G^2*Mt+v^4*R_c^2))/v^2->

    r_p<0 对本问题没有物理意义，因此可以忽略。->

    r_p=(-G*Mt)/v^2 + sqrt(G^2*Mt^2/v^4 + R_c^2)

   (e) 需要求解 R_c。由于研究的是撞击，因此令 r_p=Rt

    Rt + G*Mt/v^2 = sqrt(G^2*Mt^2/v^4 + R_c^2)->

    (Rt + G*Mt/v^2)^2 = G^2*Mt^2/v^4 + R_c^2->

    Rt^2 + 2*G*Mt*Rt/v^2 + G^2*Mt^2/v^4 = G^2*Mt^2/v^4 + R_c^2->

    Rt**2 + 2*G*Mt*Rt/v**2 = R_c**2->

    Rt**2 * (1 + 2*G*Mt/Rt *1/v**2) = R_c**2->

    逃逸速度 = sqrt(2GM/R)= v_escape**2=2GM/R->

    Rt**2 * (1 + v_esc**2/v**2) = R_c**2->

(6)
    R_capture = Rt * sqrt(1 + v_esc**2/v**2)

来源：Problem Set 3 #8 c.Fall_2017|Honors Astronomy|Professor Rachel Bezanson

来源 #2：http://www.nssc.ac.cn/wxzygx/weixin/201607/P020160718380095698873.pdf
           8.8 Planetary Rendezvous: Pg.368
"""
