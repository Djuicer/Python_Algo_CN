"""Author Alexandre De Zotti

绘制二次多项式和指数映射的朱利亚集（Julia Set）。具体而言，将函数迭代固定次数，
然后绘制最后一次迭代值的绝对值是否大于固定阈值（称为“逃逸半径”）。对于指数
映射，这并非真正的逃逸半径，而是近似具有有界轨道的朱利亚集的一种便捷方法。

此处给出的示例包括：
- 花椰菜朱利亚集，例如参见
https://en.wikipedia.org/wiki/File:Julia_z2%2B0,25.png
- https://en.wikipedia.org/wiki/Julia_set 中的其他示例
- 一个指数映射朱利亚集，在环境空间中与以下示例同胚
https://www.math.univ-toulouse.fr/~cheritat/GalII/galery.html
 and
https://ddd.uab.cat/pub/pubmat/02141493v43n1/02141493v43n1p27.pdf

备注：部分运行时溢出警告会被抑制，这是因为迭代循环使用了 numpy 的高效计算
实现。每一步之后，溢出值和无穷值都会被一个大数替换。
"""

import warnings
from collections.abc import Callable
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

c_cauliflower = 0.25 + 0.0j
c_polynomial_1 = -0.4 + 0.6j
c_polynomial_2 = -0.1 + 0.651j
c_exponential = -2.0
nb_iterations = 56
window_size = 2.0
nb_pixels = 666


def eval_exponential(c_parameter: complex, z_values: np.ndarray) -> np.ndarray:
    """
    计算 $e^z + c$。
    >>> float(eval_exponential(0, 0))
    1.0
    >>> bool(abs(eval_exponential(1, np.pi*1.j)) < 1e-15)
    True
    >>> bool(abs(eval_exponential(1.j, 0)-1-1.j) < 1e-15)
    True
    """
    return np.exp(z_values) + c_parameter


def eval_quadratic_polynomial(c_parameter: complex, z_values: np.ndarray) -> np.ndarray:
    """
    >>> eval_quadratic_polynomial(0, 2)
    4
    >>> eval_quadratic_polynomial(-1, 1)
    0
    >>> round(eval_quadratic_polynomial(1.j, 0).imag)
    1
    >>> round(eval_quadratic_polynomial(1.j, 0).real)
    0
    """
    return z_values * z_values + c_parameter


def prepare_grid(window_size: float, nb_pixels: int) -> np.ndarray:
    """
    创建大小为 nb_pixels*nb_pixels 的复数网格，实部和虚部范围均为
    -window_size 到 window_size（含端点）。返回 numpy 数组。

    >>> prepare_grid(1,3)
    array([[-1.-1.j, -1.+0.j, -1.+1.j],
           [ 0.-1.j,  0.+0.j,  0.+1.j],
           [ 1.-1.j,  1.+0.j,  1.+1.j]])
    """
    x = np.linspace(-window_size, window_size, nb_pixels)
    x = x.reshape((nb_pixels, 1))
    y = np.linspace(-window_size, window_size, nb_pixels)
    y = y.reshape((1, nb_pixels))
    return x + 1.0j * y


def iterate_function(
    eval_function: Callable[[Any, np.ndarray], np.ndarray],
    function_params: Any,
    nb_iterations: int,
    z_0: np.ndarray,
    infinity: float | None = None,
) -> np.ndarray:
    """
    将函数 "eval_function" 恰好迭代 nb_iterations 次。函数的第一个参数包含在
    function_params 中。变量 z_0 是包含迭代初值的数组。本函数返回最终迭代值。

    >>> iterate_function(eval_quadratic_polynomial, 0, 3, np.array([0,1,2])).shape
    (3,)
    >>> complex(np.round(iterate_function(eval_quadratic_polynomial,
    ... 0,
    ... 3,
    ... np.array([0,1,2]))[0]))
    0j
    >>> complex(np.round(iterate_function(eval_quadratic_polynomial,
    ... 0,
    ... 3,
    ... np.array([0,1,2]))[1]))
    (1+0j)
    >>> complex(np.round(iterate_function(eval_quadratic_polynomial,
    ... 0,
    ... 3,
    ... np.array([0,1,2]))[2]))
    (256+0j)
    """

    z_n = z_0.astype("complex64")
    for _ in range(nb_iterations):
        z_n = eval_function(function_params, z_n)
        if infinity is not None:
            np.nan_to_num(z_n, copy=False, nan=infinity)
            z_n[abs(z_n) == np.inf] = infinity
    return z_n


def show_results(
    function_label: str,
    function_params: Any,
    escape_radius: float,
    z_final: np.ndarray,
) -> None:
    """
    绘制 z_final 的绝对值是否大于 escape_radius，并将 function_label 和
    function_params 添加到标题中。

    >>> show_results('80', 0, 1, np.array([[0,1,.5],[.4,2,1.1],[.2,1,1.3]]))
    """

    abs_z_final = (abs(z_final)).transpose()
    abs_z_final[:, :] = abs_z_final[::-1, :]
    plt.matshow(abs_z_final < escape_radius)
    plt.title(f"Julia set of ${function_label}$, $c={function_params}$")
    plt.show()


def ignore_overflow_warnings() -> None:
    """
    忽略部分溢出和无效值警告。

    >>> ignore_overflow_warnings()
    """
    warnings.filterwarnings(
        "ignore", category=RuntimeWarning, message="overflow encountered in multiply"
    )
    warnings.filterwarnings(
        "ignore",
        category=RuntimeWarning,
        message="invalid value encountered in multiply",
    )
    warnings.filterwarnings(
        "ignore", category=RuntimeWarning, message="overflow encountered in absolute"
    )
    warnings.filterwarnings(
        "ignore", category=RuntimeWarning, message="overflow encountered in exp"
    )


if __name__ == "__main__":
    z_0 = prepare_grid(window_size, nb_pixels)

    ignore_overflow_warnings()  # 说明参见文件头部

    nb_iterations = 24
    escape_radius = 2 * abs(c_cauliflower) + 1
    z_final = iterate_function(
        eval_quadratic_polynomial,
        c_cauliflower,
        nb_iterations,
        z_0,
        infinity=1.1 * escape_radius,
    )
    show_results("z^2+c", c_cauliflower, escape_radius, z_final)

    nb_iterations = 64
    escape_radius = 2 * abs(c_polynomial_1) + 1
    z_final = iterate_function(
        eval_quadratic_polynomial,
        c_polynomial_1,
        nb_iterations,
        z_0,
        infinity=1.1 * escape_radius,
    )
    show_results("z^2+c", c_polynomial_1, escape_radius, z_final)

    nb_iterations = 161
    escape_radius = 2 * abs(c_polynomial_2) + 1
    z_final = iterate_function(
        eval_quadratic_polynomial,
        c_polynomial_2,
        nb_iterations,
        z_0,
        infinity=1.1 * escape_radius,
    )
    show_results("z^2+c", c_polynomial_2, escape_radius, z_final)

    nb_iterations = 12
    escape_radius = 10000.0
    z_final = iterate_function(
        eval_exponential,
        c_exponential,
        nb_iterations,
        z_0 + 2,
        infinity=1.0e10,
    )
    show_results("e^z+c", c_exponential, escape_radius, z_final)
