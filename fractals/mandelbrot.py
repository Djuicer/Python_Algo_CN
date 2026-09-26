"""
曼德勃罗集（Mandelbrot Set）是使序列 "z_(n+1) = z_n * z_n + c" 不发散（即保持
有界）的复数 "c" 的集合。因此，从 "z_0 = 0" 开始反复迭代时，如果对所有
"n > 0"，"z_n" 的绝对值始终有界，则复数 "c" 属于曼德勃罗集。复数可写作
"a + b*i"："a" 是实部，通常绘制在 x 轴上；"b*i" 是虚部，通常绘制在 y 轴上。
大多数曼德勃罗集可视化使用颜色编码，表示集合外的数在序列迭代多少步后发散。
曼德勃罗集图像具有精巧且无限复杂的边界；随着放大倍数增加，边界会逐渐展现
更精细的递归细节，因此曼德勃罗集的边界是一条分形曲线。
（说明改编自 https://en.wikipedia.org/wiki/Mandelbrot_set ）
（另请参阅 https://en.wikipedia.org/wiki/Plotting_algorithms_for_the_Mandelbrot_set ）
"""

import colorsys

from PIL import Image


def get_distance(x: float, y: float, max_step: int) -> float:
    """
    返回由此 x-y 对构成的复数发散时的相对距离（= step/max_step）。曼德勃罗集
    中的成员不会发散，因此其距离为 1。

    >>> get_distance(0, 0, 50)
    1.0
    >>> get_distance(0.5, 0.5, 50)
    0.061224489795918366
    >>> get_distance(2, 0, 50)
    0.0
    """
    a = x
    b = y
    for step in range(max_step):  # noqa: B007
        a_new = a * a - b * b + x
        b = 2 * a * b + y
        a = a_new

        # 所有绝对值大于 4 的复数都会发散
        if a * a + b * b > 4:
            break
    return step / (max_step - 1)


def get_black_and_white_rgb(distance: float) -> tuple:
    """
    忽略相对距离的黑白颜色编码。曼德勃罗集为黑色，其余部分为白色。

    >>> get_black_and_white_rgb(0)
    (255, 255, 255)
    >>> get_black_and_white_rgb(0.5)
    (255, 255, 255)
    >>> get_black_and_white_rgb(1)
    (0, 0, 0)
    """
    if distance == 1:
        return (0, 0, 0)
    else:
        return (255, 255, 255)


def get_color_coded_rgb(distance: float) -> tuple:
    """
    考虑相对距离的颜色编码。曼德勃罗集为黑色。

    >>> get_color_coded_rgb(0)
    (255, 0, 0)
    >>> get_color_coded_rgb(0.5)
    (0, 255, 255)
    >>> get_color_coded_rgb(1)
    (0, 0, 0)
    """
    if distance == 1:
        return (0, 0, 0)
    else:
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(distance, 1, 1))


def get_image(
    image_width: int = 800,
    image_height: int = 600,
    figure_center_x: float = -0.6,
    figure_center_y: float = 0,
    figure_width: float = 3.2,
    max_step: int = 50,
    use_distance_color_coding: bool = True,
) -> Image.Image:
    """
    生成曼德勃罗集图像。使用两类坐标：表示像素的图像坐标，以及表示曼德勃罗集
    内外复数的图形坐标。函数参数中的图形坐标决定查看曼德勃罗集的哪个区域。
    在图形坐标中，曼德勃罗集的主要区域大致位于 "-1.5 < x < 0.5" 和
    "-1 < y < 1" 之间。
    注释掉会拖慢 pytest 的测试……
    # 13.35s call     fractals/mandelbrot.py::mandelbrot.get_image
    # >>> get_image().load()[0,0]
    (255, 0, 0)
    # >>> get_image(use_distance_color_coding = False).load()[0,0]
    (255, 255, 255)
    """
    img = Image.new("RGB", (image_width, image_height))
    pixels = img.load()
    assert pixels is not None

    # 遍历图像坐标
    for image_x in range(image_width):
        for image_y in range(image_height):
            # 根据图像坐标确定图形坐标
            figure_height = figure_width / image_width * image_height
            figure_x = figure_center_x + (image_x / image_width - 0.5) * figure_width
            figure_y = figure_center_y + (image_y / image_height - 0.5) * figure_height

            distance = get_distance(figure_x, figure_y, max_step)

            # 根据所选着色函数为对应像素着色
            if use_distance_color_coding:
                pixels[image_x, image_y] = get_color_coded_rgb(distance)
            else:
                pixels[image_x, image_y] = get_black_and_white_rgb(distance)

    return img


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # 彩色版本，完整图形
    img = get_image()

    # 取消注释可查看彩色版本的另一放大区域
    # img = get_image(figure_center_x = -0.6, figure_center_y = -0.4,
    # figure_width = 0.8)

    # 取消注释可查看黑白版本的完整图形
    # img = get_image(use_distance_color_coding = False)

    # 取消注释可保存图像
    # img.save("mandelbrot.png")

    img.show()
