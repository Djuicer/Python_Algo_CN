"""
模拟一条环形单车道公路的演化。公路被划分为多个元胞，每个元胞最多容纳
一辆汽车。由于公路呈环形，汽车到达一端后会从另一端出现。
每辆汽车用其速度（0 到 5）表示。

速度说明：
    -1 表示公路上的元胞为空
    0 到 5 表示汽车速度，其中 0 最低，5 最高

highway: list[int]  存储每辆汽车的位置和速度
probability         驾驶员减速的概率
initial_speed       汽车的初始速度
frequency           初始状态下两辆汽车之间的元胞数
max_speed           汽车能够达到的最大速度
number_of_cells     公路中的元胞数量
number_of_update    位置更新次数

更多信息：https://en.wikipedia.org/wiki/Nagel%E2%80%93Schreckenberg_model

doctest 示例：
>>> simulate(construct_highway(6, 3, 0), 2, 0, 2)
[[0, -1, -1, 0, -1, -1], [-1, 1, -1, -1, 1, -1], [-1, -1, 1, -1, -1, 1]]
>>> simulate(construct_highway(5, 2, -2), 3, 0, 2)
[[0, -1, 0, -1, 0], [0, -1, 0, -1, -1], [0, -1, -1, 1, -1], [-1, 1, -1, 0, -1]]
"""

from random import randint, random


def construct_highway(
    number_of_cells: int,
    frequency: int,
    initial_speed: int,
    random_frequency: bool = False,
    random_speed: bool = False,
    max_speed: int = 5,
) -> list:
    """
    根据给定参数构建公路。
    >>> construct_highway(10, 2, 6)
    [[6, -1, 6, -1, 6, -1, 6, -1, 6, -1]]
    >>> construct_highway(10, 10, 2)
    [[2, -1, -1, -1, -1, -1, -1, -1, -1, -1]]
    """

    highway = [[-1] * number_of_cells]  # 创建一条没有汽车的公路
    i = 0
    initial_speed = max(initial_speed, 0)
    while i < number_of_cells:
        highway[0][i] = (
            randint(0, max_speed) if random_speed else initial_speed
        )  # 放置汽车
        i += (
            randint(1, max_speed * 2) if random_frequency else frequency
        )  # 任意数值，可能需要调整
    return highway


def get_distance(highway_now: list, car_index: int) -> int:
    """
    获取一辆汽车（索引为 car_index）与下一辆汽车之间的距离。
    >>> get_distance([6, -1, 6, -1, 6], 2)
    1
    >>> get_distance([2, -1, -1, -1, 3, 1, 0, 1, 3, 2], 0)
    3
    >>> get_distance([-1, -1, -1, -1, 2, -1, -1, -1, 3], -1)
    4
    """

    distance = 0
    cells = highway_now[car_index + 1 :]
    for cell in range(len(cells)):  # 此变量或许需要更合适的名称
        if cells[cell] != -1:  # 如果元胞非空
            return distance  # 得到所需距离
        distance += 1
    # 汽车靠近公路末端时执行到此处
    return distance + get_distance(highway_now, -1)


def update(highway_now: list, probability: float, max_speed: int) -> list:
    """
    更新汽车速度。
    >>> update([-1, -1, -1, -1, -1, 2, -1, -1, -1, -1, 3], 0.0, 5)
    [-1, -1, -1, -1, -1, 3, -1, -1, -1, -1, 4]
    >>> update([-1, -1, 2, -1, -1, -1, -1, 3], 0.0, 5)
    [-1, -1, 3, -1, -1, -1, -1, 1]
    """

    number_of_cells = len(highway_now)
    # 计算前，下一时刻的公路为空
    next_highway = [-1] * number_of_cells

    for car_index in range(number_of_cells):
        if highway_now[car_index] != -1:
            # 当前车速加 1，并限制最大速度
            next_highway[car_index] = min(highway_now[car_index] + 1, max_speed)
            # 与下一辆汽车之间的空元胞数量
            dn = get_distance(highway_now, car_index) - 1
            # 防止汽车发生碰撞
            next_highway[car_index] = min(next_highway[car_index], dn)
            if random() < probability:
                # 驾驶员随机减速
                next_highway[car_index] = max(next_highway[car_index] - 1, 0)
    return next_highway


def simulate(
    highway: list, number_of_update: int, probability: float, max_speed: int
) -> list:
    """
    模拟公路演化的主函数。
    >>> simulate([[-1, 2, -1, -1, -1, 3]], 2, 0.0, 3)
    [[-1, 2, -1, -1, -1, 3], [-1, -1, -1, 2, -1, 0], [1, -1, -1, 0, -1, -1]]
    >>> simulate([[-1, 2, -1, 3]], 4, 0.0, 3)
    [[-1, 2, -1, 3], [-1, 0, -1, 0], [-1, 0, -1, 0], [-1, 0, -1, 0], [-1, 0, -1, 0]]
    """

    number_of_cells = len(highway[0])

    for i in range(number_of_update):
        next_speeds_calculated = update(highway[i], probability, max_speed)
        real_next_speeds = [-1] * number_of_cells

        for car_index in range(number_of_cells):
            speed = next_speeds_calculated[car_index]
            if speed != -1:
                # 根据速度改变位置（使用 % 构成环形）
                index = (car_index + speed) % number_of_cells
                # 应用位置变化
                real_next_speeds[index] = speed
        highway.append(real_next_speeds)

    return highway


if __name__ == "__main__":
    import doctest

    doctest.testmod()
