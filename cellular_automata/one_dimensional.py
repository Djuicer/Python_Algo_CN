"""
根据给定的规则集编号，返回一维元胞自动机 16 代状态的图像。
https://mathworld.wolfram.com/ElementaryCellularAutomaton.html
"""

from __future__ import annotations

from PIL import Image

# 定义第一代元胞
# fmt: off
CELLS = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
# fmt: on


def format_ruleset(ruleset: int) -> list[int]:
    """
    >>> format_ruleset(11100)
    [0, 0, 0, 1, 1, 1, 0, 0]
    >>> format_ruleset(0)
    [0, 0, 0, 0, 0, 0, 0, 0]
    >>> format_ruleset(11111111)
    [1, 1, 1, 1, 1, 1, 1, 1]
    """
    return [int(c) for c in f"{ruleset:08}"[:8]]


def new_generation(cells: list[list[int]], rule: list[int], time: int) -> list[int]:
    population = len(cells[0])  # 31
    next_generation = []
    for i in range(population):
        # 获取每个元胞的邻居
        # 将边界外邻居的值视为 0
        left_neighbor = 0 if i == 0 else cells[time][i - 1]
        right_neighbor = 0 if i == population - 1 else cells[time][i + 1]
        # 定义新元胞并将其加入下一代
        situation = 7 - int(f"{left_neighbor}{cells[time][i]}{right_neighbor}", 2)
        next_generation.append(rule[situation])
    return next_generation


def generate_image(cells: list[list[int]]) -> Image.Image:
    """
    将元胞转换为灰度 PIL.Image.Image，并返回给调用方。
    >>> from random import random
    >>> cells = [[random() for w in range(31)] for h in range(16)]
    >>> img = generate_image(cells)
    >>> isinstance(img, Image.Image)
    True
    >>> img.width, img.height
    (31, 16)
    """
    # 创建输出图像
    img = Image.new("RGB", (len(cells[0]), len(cells)))
    pixels = img.load()
    assert pixels is not None
    # 生成图像
    for w in range(img.width):
        for h in range(img.height):
            color = 255 - int(255 * cells[h][w])
            pixels[w, h] = (color, color, color)
    return img


if __name__ == "__main__":
    rule_num = bin(int(input("Rule:\n").strip()))[2:]
    rule = format_ruleset(int(rule_num))
    for time in range(16):
        CELLS.append(new_generation(CELLS, rule, time))
    img = generate_image(CELLS)
    # 取消注释以保存图像
    # img.save(f"rule_{rule_num}.png")
    img.show()
