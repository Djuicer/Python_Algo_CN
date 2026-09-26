"""
本模块包含计算透镜焦距、像距和物距的函数，均使用透镜公式计算。

在光学中，像距 (v)、物距 (u) 与透镜焦距 (f) 之间的关系由透镜公式给出。
该公式同时适用于凸透镜和凹透镜：

-------------------
| 1/f = 1/v + 1/u |
-------------------

其中：
    f = 透镜焦距，单位为米。
    v = 像到透镜的距离，单位为米。
    u = 物体到透镜的距离，单位为米。

为简化计算，推导公式时作出以下假设，求解前应加以注意：
    1. 物体 O 是位于主轴上的点物体。
    2. 透镜为薄透镜。
    3. 透镜孔径必须较小。
    4. 入射角和折射角应较小。

符号约定是一组为像距、物距、焦距等确定正负号的规则，用于成像的数学分析：
    1. 物体始终置于透镜左侧。
    2. 所有距离均从光心量起。
    3. 沿入射光线方向测量的距离为正，反向测量的距离为负。
    4. 沿 y 轴、主轴上方测得的距离为正，主轴下方为负。

注意：符号约定也可反转，仍会得到正确结果。

符号约定参考资料：
https://www.toppr.com/ask/content/concept/sign-convention-for-lenses-210246/

假设参考资料：
https://testbook.com/physics/derivation-of-lens-maker-formula
"""


def focal_length_of_lens(
    object_distance_from_lens: float, image_distance_from_lens: float
) -> float:
    """
    Doctest：
    >>> from math import isclose
    >>> isclose(focal_length_of_lens(10,4), 6.666666666666667)
    True
    >>> from math import isclose
    >>> isclose(focal_length_of_lens(2.7,5.8), -5.0516129032258075)
    True
    >>> focal_length_of_lens(0, 20)  # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    ValueError: Invalid inputs. Enter non zero values with respect
    to the sign convention.
    """

    if object_distance_from_lens == 0 or image_distance_from_lens == 0:
        raise ValueError(
            "Invalid inputs. Enter non zero values with respect to the sign convention."
        )
    focal_length = 1 / (
        (1 / image_distance_from_lens) - (1 / object_distance_from_lens)
    )
    return focal_length


def object_distance(
    focal_length_of_lens: float, image_distance_from_lens: float
) -> float:
    """
    Doctest：
    >>> from math import isclose
    >>> isclose(object_distance(10,40), -13.333333333333332)
    True

    >>> from math import isclose
    >>> isclose(object_distance(6.2,1.5), 1.9787234042553192)
    True

    >>> object_distance(0, 20)  # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    ValueError: Invalid inputs. Enter non zero values with respect
    to the sign convention.
    """

    if image_distance_from_lens == 0 or focal_length_of_lens == 0:
        raise ValueError(
            "Invalid inputs. Enter non zero values with respect to the sign convention."
        )

    object_distance = 1 / ((1 / image_distance_from_lens) - (1 / focal_length_of_lens))
    return object_distance


def image_distance(
    focal_length_of_lens: float, object_distance_from_lens: float
) -> float:
    """
    Doctest：
    >>> from math import isclose
    >>> isclose(image_distance(50,40), 22.22222222222222)
    True
    >>> from math import isclose
    >>> isclose(image_distance(5.3,7.9), 3.1719696969696973)
    True

    >>> object_distance(0, 20)  # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    ValueError: Invalid inputs. Enter non zero values with respect
    to the sign convention.
    """
    if object_distance_from_lens == 0 or focal_length_of_lens == 0:
        raise ValueError(
            "Invalid inputs. Enter non zero values with respect to the sign convention."
        )
    image_distance = 1 / ((1 / object_distance_from_lens) + (1 / focal_length_of_lens))
    return image_distance
