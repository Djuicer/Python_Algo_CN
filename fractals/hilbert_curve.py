"""
Author Atharva Date | atharvad931@gmail.com | git/Atharva9621

希尔伯特曲线（Hilbert Curve，也称希尔伯特空间填充曲线）是一条连续的分形空间
填充曲线，也是空间填充皮亚诺曲线的一种变体。

由于它能填充空间，其豪斯多夫维数为 2。准确地说，其像是单位正方形，在任何维数
定义下维数均为 2。它的图像是与闭单位区间同胚的紧集，豪斯多夫维数为 1。

致谢：
    说明改编自
    https://en.wikipedia.org/wiki/Hilbert_curve

    另请参阅
    https://youtu.be/3s7h2MHQtxc?si=_qIusAJFHYfXIOKn
        (3b1b - Hilbert's Curve: Is infinite math useful?)
    https://dl.acm.org/doi/pdf/10.1145/290200.290219

依赖（pip）：
    - matplotlib
"""

import matplotlib.pyplot as plt


def rotate_pnts(
    pnts: list[tuple[float, float]], angle: int
) -> list[tuple[float, float]]:
    """
    将点列表旋转给定角度（角度为 90 度的倍数）。

    由于旋转仅限于 90 度的倍数（90、180、270、360），此函数只需相应地重新排列
    点列表。每个象限中的旋转通过调整列表起始索引并循环回绕来实现。

    参数：
    -----------
    pnts : List[Tuple[float, float]]
        元组列表，每个元组表示一个点 (x, y)。
    angle : int
        旋转角度，应为 90 度的倍数（例如 90、180、270、360）。

    返回值：
    --------
    List[Tuple[float, float]]
        按指定角度旋转后重新排序的点列表。

    示例：
    --------
    >>> rotate_pnts([(1, 1), (0, 1), (0, 0), (1, 0)], 90)
    [(0, 1), (0, 0), (1, 0), (1, 1)]
    """
    start_index = angle // 90 % 4
    return pnts[start_index:] + pnts[:start_index]


def hilbert_curve(
    center: tuple[float, float], level: int, side: float = 1, angle: int = 90
) -> list[tuple[float, float]]:
    """
    参数：
    ------
        center: Tuple[float, float]- 子区域的中心坐标 (x, y)。
        level: int- 希尔伯特曲线的递归深度或细分层级。
        side : float, optional
                绘制曲线的正方形区域边长。
        angle : int, optional
                曲线的初始旋转角度，单位为度。
                应为 90 度的倍数。（default=90）

    返回值：
    ------
        pts: List[Tuple[float, float]] -
            表示给定层级希尔伯特曲线的点 (x, y) 列表。

    示例：
    --------
    >>> hilbert_curve((0, 0), 1, angle=0)
    [(0.25, 0.25), (-0.25, 0.25), (-0.25, -0.25), (0.25, -0.25)]
    """
    x, y = center
    angle = angle % 360
    pnts = [
        (x + side / 4, y + side / 4),
        (x - side / 4, y + side / 4),
        (x - side / 4, y - side / 4),
        (x + side / 4, y - side / 4),
    ]
    pnts = rotate_pnts(pnts, angle)

    if level == 1:
        return pnts
    else:
        return (
            hilbert_curve(pnts[0], level - 1, side / 2, angle=angle + 90)[::-1]
            + hilbert_curve(pnts[1], level - 1, side / 2, angle=angle)
            + hilbert_curve(pnts[2], level - 1, side / 2, angle=angle)
            + hilbert_curve(pnts[3], level - 1, side / 2, angle=angle - 90)[::-1]
        )


def plot_hilbert_curve(points: list[tuple[float, float]]) -> None:
    """
    使用 matplotlib 绘制希尔伯特曲线。

    示例
    --------
    >>> plot_hilbert_curve([(-0.25, 0.25), (-0.25, -0.25), (0.25, -0.25), (0.25, 0.25)])
    """
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]

    plt.plot(x_coords, y_coords, marker="o", linestyle="-")
    plt.gca().set_aspect("equal", adjustable="box")  # 使绘图区为正方形
    plt.title("Hilbert Curve")
    plt.show()


if __name__ == "__main__":
    import doctest

    # 运行 doctest
    doctest.testmod()

    # 绘制希尔伯特曲线
    plot_hilbert_curve(hilbert_curve((0, 0), 4))
