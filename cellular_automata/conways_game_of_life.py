"""
使用 Python 实现的康威生命游戏（Conway's Game of Life）。
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
"""

from __future__ import annotations

from PIL import Image

# 定义滑翔机示例
GLIDER = [
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

# 定义闪烁器示例
BLINKER = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]


def new_generation(cells: list[list[int]]) -> list[list[int]]:
    """
    根据康威生命游戏的给定状态生成下一代。
    >>> new_generation(BLINKER)
    [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    """
    next_generation = []
    for i in range(len(cells)):
        next_generation_row = []
        for j in range(len(cells[i])):
            # 获取活细胞邻居的数量
            neighbour_count = 0
            if i > 0 and j > 0:
                neighbour_count += cells[i - 1][j - 1]
            if i > 0:
                neighbour_count += cells[i - 1][j]
            if i > 0 and j < len(cells[i]) - 1:
                neighbour_count += cells[i - 1][j + 1]
            if j > 0:
                neighbour_count += cells[i][j - 1]
            if j < len(cells[i]) - 1:
                neighbour_count += cells[i][j + 1]
            if i < len(cells) - 1 and j > 0:
                neighbour_count += cells[i + 1][j - 1]
            if i < len(cells) - 1:
                neighbour_count += cells[i + 1][j]
            if i < len(cells) - 1 and j < len(cells[i]) - 1:
                neighbour_count += cells[i + 1][j + 1]

            # 生命游戏规则（摘自 Wikipedia）：
            # 1. 具有两个或三个活细胞邻居的活细胞继续存活。
            # 2. 具有三个活细胞邻居的死细胞变为活细胞。
            # 3. 其他活细胞在下一代死亡，其他死细胞仍保持死亡。
            alive = cells[i][j] == 1
            if (alive and 2 <= neighbour_count <= 3) or (
                not alive and neighbour_count == 3
            ):
                next_generation_row.append(1)
            else:
                next_generation_row.append(0)

        next_generation.append(next_generation_row)
    return next_generation


def generate_images(cells: list[list[int]], frames: int) -> list[Image.Image]:
    """
    生成生命游戏后续状态的图像列表。
    """
    images = []
    for _ in range(frames):
        # 创建输出图像
        img = Image.new("RGB", (len(cells[0]), len(cells)))
        pixels = img.load()
        assert pixels is not None

        # 将细胞状态保存到图像中
        for x in range(len(cells)):
            for y in range(len(cells[0])):
                colour = 255 - cells[y][x] * 255
                pixels[x, y] = (colour, colour, colour)

        # 保存图像
        images.append(img)
        cells = new_generation(cells)
    return images


if __name__ == "__main__":
    images = generate_images(GLIDER, 16)
    images[0].save("out.gif", save_all=True, append_images=images[1:])
