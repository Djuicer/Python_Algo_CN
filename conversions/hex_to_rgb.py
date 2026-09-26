"""
* Author: Cicero Tiago Carneiro Valentim (https://github.com/cicerotcv)
* 说明：将十六进制颜色（#FF2000）转换为 RGB（rgb(255, 32, 0)）。

参考资料：
https://www.w3schools.com/colors/colors_rgb.asp
https://www.w3schools.com/colors/colors_hexadecimal.asp
"""


def hex_to_rgb(hex_color: str) -> str:
    """
    将十六进制颜色代码转换为 RGB 值。

    参数：
        hex_color (str)：十六进制颜色代码，例如 "#RGB" 或 "#RRGGBB"。

    返回：
        str：包含三个整数的 RGB 值字符串表示 "rgb(r, g, b)"。

    异常：
        ValueError：当输入 hex_color 不是有效的十六进制颜色代码时。

    示例：
    >>> hex_to_rgb("#FF0000")
    'rgb(255, 0, 0)'

    >>> hex_to_rgb("#00FF00")
    'rgb(0, 255, 0)'

    >>> hex_to_rgb("#123")
    'rgb(17, 34, 51)'

    >>> hex_to_rgb("#000000")
    'rgb(0, 0, 0)'

    >>> hex_to_rgb("#FFFFFF")
    'rgb(255, 255, 255)'

    >>> hex_to_rgb("#0088FF")
    'rgb(0, 136, 255)'

    >>> hex_to_rgb("#0032ccAA")
    Traceback (most recent call last):
    ...
    ValueError: Invalid hex color code

    >>> hex_to_rgb("#0032")
    Traceback (most recent call last):
    ...
    ValueError: Invalid hex color code

    注意：
        - 此函数支持 6 位和 3 位十六进制颜色代码。
    """

    hex_color = hex_color.lstrip("#")

    # 检查输入是否为有效的十六进制颜色代码
    if not (len(hex_color) == 6 or len(hex_color) == 3):
        raise ValueError("Invalid hex color code")

    # 将 3 位十六进制代码扩展为 6 位（例如将 "#123" 扩展为 "#112233"）
    if len(hex_color) == 3:
        hex_color = "".join([char * 2 for char in hex_color])

    # 将十六进制值解析为整数
    red = int(hex_color[0:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:6], 16)

    return f"rgb({red}, {green}, {blue})"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
