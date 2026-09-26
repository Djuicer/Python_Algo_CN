"""
巴恩斯利蕨（Barnsley Fern）是一种形似铁角蕨的分形。英国数学家 Michael Barnsley
在 1988 年出版的 *Fractals Everywhere* 一书中对其进行了描述；它是迭代函数系统
（IFS）的经典示例。

IFS 通过反复应用一小组仿射变换来构造分形，每次按固定概率随机选择一种变换。
从点 ``(0, 0)`` 开始，该蕨形使用四种变换：

===============  ===========================================  ============
变换             效果                                         概率
===============  ===========================================  ============
茎               收缩到 y 轴                                  1%
连续叶片         蕨形的主要自相似副本                         85%
左侧小叶         较小的旋转/反射副本                          7%
右侧小叶         另一个较小的旋转/反射副本                   7%
===============  ===========================================  ============

由于整幅图像由随机过程生成，下面的 doctest 会为 Python 随机数生成器设置种子，
以使结果可复现。使用 matplotlib 绘制这些点是可选操作，仅在直接运行模块时进行。

参考资料：https://en.wikipedia.org/wiki/Barnsley_fern
"""

import random

# 每行是仿射映射的 (a, b, c, d, e, f)
#   x' = a*x + b*y + e
#   y' = c*x + d*y + f
# 以及用于选择变换的累计概率。
TRANSFORMATIONS: tuple[tuple[float, float, float, float, float, float], ...] = (
    (0.00, 0.00, 0.00, 0.16, 0.00, 0.00),  # 茎
    (0.85, 0.04, -0.04, 0.85, 0.00, 1.60),  # 连续的小叶
    (0.20, -0.26, 0.23, 0.22, 0.00, 1.60),  # 左侧小叶
    (-0.15, 0.28, 0.26, 0.24, 0.00, 0.44),  # 右侧小叶
)
CUMULATIVE_PROBABILITIES: tuple[float, ...] = (0.01, 0.86, 0.93, 1.00)


def transform(point: tuple[float, float], index: int) -> tuple[float, float]:
    """
    对 ``point`` 应用索引为 ``index`` 的仿射变换，并返回像点。

    >>> transform((0.0, 0.0), 0)
    (0.0, 0.0)
    >>> transform((1.0, 1.0), 1)
    (0.89, 2.41)
    >>> transform((2.0, 3.0), 3)
    (0.54, 1.68)
    >>> transform((0.0, 0.0), 4)
    Traceback (most recent call last):
        ...
    IndexError: index must be in range 0..3, got 4
    """
    if not 0 <= index < len(TRANSFORMATIONS):
        msg = f"index must be in range 0..3, got {index}"
        raise IndexError(msg)
    a, b, c, d, e, f = TRANSFORMATIONS[index]
    x, y = point
    new_x = round(a * x + b * y + e, 12)
    new_y = round(c * x + d * y + f, 12)
    return (new_x, new_y)


def choose_transformation(sample: float) -> int:
    """
    使用蕨形的累积概率，将 ``[0, 1)`` 中的 ``sample`` 映射到变换索引。

    >>> choose_transformation(0.0)
    0
    >>> choose_transformation(0.5)
    1
    >>> choose_transformation(0.9)
    2
    >>> choose_transformation(0.97)
    3
    """
    for index, threshold in enumerate(CUMULATIVE_PROBABILITIES):
        if sample < threshold:
            return index
    return len(CUMULATIVE_PROBABILITIES) - 1


def generate_fern(
    iterations: int, seed: int | None = None
) -> list[tuple[float, float]]:
    """
    从 ``(0, 0)`` 开始生成巴恩斯利蕨的 ``iterations`` 个点。

    传入 ``seed`` 可使原本随机的输出可复现，从而保证 doctest 的确定性。

    >>> points = generate_fern(5, seed=0)
    >>> len(points)
    5
    >>> points[0]
    (0.0, 0.0)
    >>> points  # doctest: +NORMALIZE_WHITESPACE
    [(0.0, 0.0), (0.0, 1.6), (0.064, 2.96),
     (0.1728, 4.11344), (0.3114176, 5.089512)]

    每个蕨形点都位于这个已知的边界框内。

    >>> cloud = generate_fern(2000, seed=42)
    >>> all(-2.182 <= x <= 2.6558 for x, _ in cloud)
    True
    >>> all(0.0 <= y <= 9.9984 for _, y in cloud)
    True
    >>> generate_fern(0)
    Traceback (most recent call last):
        ...
    ValueError: iterations must be positive, got 0
    """
    if iterations <= 0:
        msg = f"iterations must be positive, got {iterations}"
        raise ValueError(msg)
    rng = random.Random(seed)
    point = (0.0, 0.0)
    points = [point]
    for _ in range(iterations - 1):
        index = choose_transformation(rng.random())
        point = transform(point, index)
        points.append(point)
    return points


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is required to plot the fern (pip install matplotlib).")
    else:
        fern_points = generate_fern(100_000, seed=0)
        xs = [x for x, _ in fern_points]
        ys = [y for _, y in fern_points]
        plt.figure(figsize=(4, 8))
        plt.scatter(xs, ys, s=0.2, color="forestgreen")
        plt.axis("off")
        plt.title("Barnsley fern")
        plt.show()
