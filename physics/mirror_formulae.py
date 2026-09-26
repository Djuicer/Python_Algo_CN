"""
本模块包含计算球面镜焦距、物距和像距的函数。

球面镜公式描述球面镜物距 (u)、像距 (v) 和焦距 (f) 之间的关系，常用于光学中
确定镜面所成像的位置和特征。公式为：

-------------------
| 1/f = 1/v + 1/u |
-------------------

其中：
f = 球面镜焦距（米）
v = 像到镜面的距离（米）
u = 物体到镜面的距离（米）


距离的正负号遵循以下符号约定：
    1) 物体始终置于镜面左侧。
    2) 沿入射光线方向测量的距离为正，反向测量的距离为负。
    3) 所有距离均从镜面顶点量起。


使用球面镜公式时作出以下假设：
    1) 薄镜：镜面厚度相对于曲率半径可忽略，可将其视为二维表面。
    2) 球面镜：假定镜面为球形。该假设未必对所有镜面严格成立，但对多数实际
       用途是合理近似。
    3) 小角度：推导涉及的角度较小，可使用小角近似，即小角的正切近似等于
       角度本身，从而简化计算。
    4) 近轴光线：推导使用靠近主轴且与主轴夹角很小的光线，这可提高计算精度。
    5) 反射与折射定律：假定反射和折射定律成立；反射角等于入射角，入射光线
       与折射光线位于同一平面，折射遵循斯涅尔定律。

（说明和假设改编自
https://www.collegesearch.in/articles/mirror-formula-derivation)

（符号约定改编自
https://www.toppr.com/ask/content/concept/sign-convention-for-mirrors-210189/)


"""


def focal_length(distance_of_object: float, distance_of_image: float) -> float:
    """
    >>> from math import isclose
    >>> isclose(focal_length(10, 20), 6.66666666666666)
    True
    >>> from math import isclose
    >>> isclose(focal_length(9.5, 6.7), 3.929012346)
    True
    >>> focal_length(0, 20)  # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    ValueError: Invalid inputs. Enter non zero values with respect
    to the sign convention.
    """

    if distance_of_object == 0 or distance_of_image == 0:
        raise ValueError(
            "Invalid inputs. Enter non zero values with respect to the sign convention."
        )
    focal_length = 1 / ((1 / distance_of_object) + (1 / distance_of_image))
    return focal_length


def object_distance(focal_length: float, distance_of_image: float) -> float:
    """
    >>> from math import isclose
    >>> isclose(object_distance(30, 20), -60.0)
    True
    >>> from math import isclose
    >>> isclose(object_distance(10.5, 11.7), 102.375)
    True
    >>> object_distance(90, 0)  # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    ValueError: Invalid inputs. Enter non zero values with respect
    to the sign convention.
    """

    if distance_of_image == 0 or focal_length == 0:
        raise ValueError(
            "Invalid inputs. Enter non zero values with respect to the sign convention."
        )
    object_distance = 1 / ((1 / focal_length) - (1 / distance_of_image))
    return object_distance


def image_distance(focal_length: float, distance_of_object: float) -> float:
    """
    >>> from math import isclose
    >>> isclose(image_distance(10, 40), 13.33333333)
    True
    >>> from math import isclose
    >>> isclose(image_distance(1.5, 6.7), 1.932692308)
    True
    >>> image_distance(0, 0)  # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    ValueError: Invalid inputs. Enter non zero values with respect
    to the sign convention.
    """

    if distance_of_object == 0 or focal_length == 0:
        raise ValueError(
            "Invalid inputs. Enter non zero values with respect to the sign convention."
        )
    image_distance = 1 / ((1 / focal_length) - (1 / distance_of_object))
    return image_distance
