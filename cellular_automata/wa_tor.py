"""
Wa-Tor 算法（1984）

| @ https://en.wikipedia.org/wiki/Wa-Tor
| @ https://beltoforion.de/en/wator/
| @ https://beltoforion.de/en/wator/images/wator_medium.webm

此解决方案旨在完全消除对 Wa-Tor 星球的任何系统化处理方式，
并采用完全随机的方法。

这些常量构成一组可用配置，使 Wa-Tor 星球产生三种可能结果之一。
"""

from collections.abc import Callable
from random import randint, shuffle
from time import sleep
from typing import Literal

WIDTH = 50  # Wa-Tor 星球的宽度
HEIGHT = 50  # Wa-Tor 星球的高度

PREY_INITIAL_COUNT = 30  # 猎物实体的初始数量
PREY_REPRODUCTION_TIME = 5  # 繁殖前需要经过的时元数

PREDATOR_INITIAL_COUNT = 50  # 捕食者实体的初始数量
# 捕食者实体的初始能量值
PREDATOR_INITIAL_ENERGY_VALUE = 15
# 吃掉猎物时获得的能量值
PREDATOR_FOOD_VALUE = 5
PREDATOR_REPRODUCTION_TIME = 20  # 繁殖前需要经过的时元数

MAX_ENTITIES = 500  # 棋盘上的最大生物数量
# 从数量失衡的一方删除的实体数
DELETE_UNBALANCED_ENTITIES = 50


class Entity:
    """
    表示一个实体（猎物或捕食者）。

    >>> e = Entity(True, coords=(0, 0))
    >>> e.prey
    True
    >>> e.coords
    (0, 0)
    >>> e.alive
    True
    """

    def __init__(self, prey: bool, coords: tuple[int, int]) -> None:
        self.prey = prey
        # 实体的 (row, col) 位置
        self.coords = coords

        self.remaining_reproduction_time = (
            PREY_REPRODUCTION_TIME if prey else PREDATOR_REPRODUCTION_TIME
        )
        self.energy_value = None if prey is True else PREDATOR_INITIAL_ENERGY_VALUE
        self.alive = True

    def reset_reproduction_time(self) -> None:
        """
        >>> e = Entity(True, coords=(0, 0))
        >>> e.reset_reproduction_time()
        >>> e.remaining_reproduction_time == PREY_REPRODUCTION_TIME
        True
        >>> e = Entity(False, coords=(0, 0))
        >>> e.reset_reproduction_time()
        >>> e.remaining_reproduction_time == PREDATOR_REPRODUCTION_TIME
        True
        """
        self.remaining_reproduction_time = (
            PREY_REPRODUCTION_TIME if self.prey is True else PREDATOR_REPRODUCTION_TIME
        )

    def __repr__(self) -> str:
        """
        >>> Entity(prey=True, coords=(1, 1))
        Entity(prey=True, coords=(1, 1), remaining_reproduction_time=5)
        >>> Entity(prey=False, coords=(2, 1))  # doctest: +NORMALIZE_WHITESPACE
        Entity(prey=False, coords=(2, 1),
        remaining_reproduction_time=20, energy_value=15)
        """
        repr_ = (
            f"Entity(prey={self.prey}, coords={self.coords}, "
            f"remaining_reproduction_time={self.remaining_reproduction_time}"
        )
        if self.energy_value is not None:
            repr_ += f", energy_value={self.energy_value}"
        return f"{repr_})"


class WaTor:
    """
    表示 Wa-Tor 主算法。

    :attr time_passed: 每当时间流逝一个时元（chronon）时调用的函数，
        用于直观显示新的 Wa-Tor 星球。`time_passed` 函数可以使用
        ``time.sleep`` 阻塞，以减缓算法的运行速度。

    >>> wt = WaTor(10, 15)
    >>> wt.width
    10
    >>> wt.height
    15
    >>> len(wt.planet)
    15
    >>> len(wt.planet[0])
    10
    >>> len(wt.get_entities()) == PREDATOR_INITIAL_COUNT + PREY_INITIAL_COUNT
    True
    """

    time_passed: Callable[["WaTor", int], None] | None

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.time_passed = None

        self.planet: list[list[Entity | None]] = [[None] * width for _ in range(height)]

        # 在星球上随机放置捕食者和猎物
        for _ in range(PREY_INITIAL_COUNT):
            self.add_entity(prey=True)
        for _ in range(PREDATOR_INITIAL_COUNT):
            self.add_entity(prey=False)
        self.set_planet(self.planet)

    def set_planet(self, planet: list[list[Entity | None]]) -> None:
        """
        便于测试时访问。

        >>> wt = WaTor(WIDTH, HEIGHT)
        >>> planet = [
        ... [None, None, None],
        ... [None, Entity(True, coords=(1, 1)), None]
        ... ]
        >>> wt.set_planet(planet)
        >>> wt.planet == planet
        True
        >>> wt.width
        3
        >>> wt.height
        2
        """
        self.planet = planet
        self.width = len(planet[0])
        self.height = len(planet)

    def add_entity(self, prey: bool) -> None:
        """
        添加一个实体，并确保该实体不会覆盖其他实体。

        >>> wt = WaTor(WIDTH, HEIGHT)
        >>> wt.set_planet([[None, None], [None, None]])
        >>> wt.add_entity(True)
        >>> len(wt.get_entities())
        1
        >>> wt.add_entity(False)
        >>> len(wt.get_entities())
        2
        """
        while True:
            row, col = randint(0, self.height - 1), randint(0, self.width - 1)
            if self.planet[row][col] is None:
                self.planet[row][col] = Entity(prey=prey, coords=(row, col))
                return

    def get_entities(self) -> list[Entity]:
        """
        返回星球中所有实体的列表。

        >>> wt = WaTor(WIDTH, HEIGHT)
        >>> len(wt.get_entities()) == PREDATOR_INITIAL_COUNT + PREY_INITIAL_COUNT
        True
        """
        return [entity for column in self.planet for entity in column if entity]

    def balance_predators_and_prey(self) -> None:
        """
        平衡捕食者与猎物的数量，防止猎物数量压倒捕食者，
        占满捕食者繁殖所需的空间。

        >>> wt = WaTor(WIDTH, HEIGHT)
        >>> for i in range(2000):
        ...     row, col = i // HEIGHT, i % WIDTH
        ...     wt.planet[row][col] = Entity(True, coords=(row, col))
        >>> entities = len(wt.get_entities())
        >>> wt.balance_predators_and_prey()
        >>> len(wt.get_entities()) == entities
        False
        """
        entities = self.get_entities()
        shuffle(entities)

        if len(entities) >= MAX_ENTITIES - MAX_ENTITIES / 10:
            prey = [entity for entity in entities if entity.prey]
            predators = [entity for entity in entities if not entity.prey]

            prey_count, predator_count = len(prey), len(predators)

            entities_to_purge = (
                prey[:DELETE_UNBALANCED_ENTITIES]
                if prey_count > predator_count
                else predators[:DELETE_UNBALANCED_ENTITIES]
            )
            for entity in entities_to_purge:
                self.planet[entity.coords[0]][entity.coords[1]] = None

    def get_surrounding_prey(self, entity: Entity) -> list[Entity]:
        """
        返回捕食者实体四周（N、S、E、W）的所有猎物实体。

        与 `move_and_reproduce` 略有不同。

        >>> wt = WaTor(WIDTH, HEIGHT)
        >>> wt.set_planet([
        ... [None, Entity(True, (0, 1)), None],
        ... [None, Entity(False, (1, 1)), None],
        ... [None, Entity(True, (2, 1)), None]])
        >>> wt.get_surrounding_prey(
        ... Entity(False, (1, 1)))  # doctest: +NORMALIZE_WHITESPACE
        [Entity(prey=True, coords=(0, 1), remaining_reproduction_time=5),
        Entity(prey=True, coords=(2, 1), remaining_reproduction_time=5)]
        >>> wt.set_planet([[Entity(False, (0, 0))]])
        >>> wt.get_surrounding_prey(Entity(False, (0, 0)))
        []
        >>> wt.set_planet([
        ... [Entity(True, (0, 0)), Entity(False, (1, 0)), Entity(False, (2, 0))],
        ... [None, Entity(False, (1, 1)), Entity(True, (2, 1))],
        ... [None, None, None]])
        >>> wt.get_surrounding_prey(Entity(False, (1, 0)))
        [Entity(prey=True, coords=(0, 0), remaining_reproduction_time=5)]
        """
        row, col = entity.coords
        adjacent: list[tuple[int, int]] = [
            (row - 1, col),  # 北
            (row + 1, col),  # 南
            (row, col - 1),  # 西
            (row, col + 1),  # 东
        ]

        return [
            ent
            for r, c in adjacent
            if 0 <= r < self.height
            and 0 <= c < self.width
            and (ent := self.planet[r][c]) is not None
            and ent.prey
        ]

    def move_and_reproduce(
        self, entity: Entity, direction_orders: list[Literal["N", "E", "S", "W"]]
    ) -> None:
        """
        尝试向四个方向（北、南、东、西）之一的相邻空方格移动。
        如果移动成功且 `remaining_reproduction_time` 等于 0，
        还可以在原方格中创建新的猎物或捕食者。

        :param direction_orders: 表示尝试移动顺序的有序列表（类似优先队列），
                            用于消除检查相邻方格时的系统化顺序。

        >>> planet = [
        ... [None, None, None],
        ... [None, Entity(True, coords=(1, 1)), None],
        ... [None, None, None]
        ... ]
        >>> wt = WaTor(WIDTH, HEIGHT)
        >>> wt.set_planet(planet)
        >>> wt.move_and_reproduce(Entity(True, coords=(1, 1)), direction_orders=["N"])
        >>> wt.planet  # doctest: +NORMALIZE_WHITESPACE
        [[None, Entity(prey=True, coords=(0, 1), remaining_reproduction_time=4), None],
        [None, None, None],
        [None, None, None]]
        >>> wt.planet[0][0] = Entity(True, coords=(0, 0))
        >>> wt.move_and_reproduce(Entity(True, coords=(0, 1)),
        ... direction_orders=["N", "W", "E", "S"])
        >>> wt.planet  # doctest: +NORMALIZE_WHITESPACE
        [[Entity(prey=True, coords=(0, 0), remaining_reproduction_time=5), None,
        Entity(prey=True, coords=(0, 2), remaining_reproduction_time=4)],
        [None, None, None],
        [None, None, None]]
        >>> wt.planet[0][1] = wt.planet[0][2]
        >>> wt.planet[0][2] = None
        >>> wt.move_and_reproduce(Entity(True, coords=(0, 1)),
        ... direction_orders=["N", "W", "S", "E"])
        >>> wt.planet  # doctest: +NORMALIZE_WHITESPACE
        [[Entity(prey=True, coords=(0, 0), remaining_reproduction_time=5), None, None],
        [None, Entity(prey=True, coords=(1, 1), remaining_reproduction_time=4), None],
        [None, None, None]]

        >>> wt = WaTor(WIDTH, HEIGHT)
        >>> reproducable_entity = Entity(False, coords=(0, 1))
        >>> reproducable_entity.remaining_reproduction_time = 0
        >>> wt.planet = [[None, reproducable_entity]]
        >>> wt.move_and_reproduce(reproducable_entity,
        ... direction_orders=["N", "W", "S", "E"])
        >>> wt.planet  # doctest: +NORMALIZE_WHITESPACE
        [[Entity(prey=False, coords=(0, 0),
        remaining_reproduction_time=20, energy_value=15),
        Entity(prey=False, coords=(0, 1), remaining_reproduction_time=20,
        energy_value=15)]]
        """
        row, col = coords = entity.coords

        adjacent_squares: dict[Literal["N", "E", "S", "W"], tuple[int, int]] = {
            "N": (row - 1, col),  # 北
            "S": (row + 1, col),  # 南
            "W": (row, col - 1),  # 西
            "E": (row, col + 1),  # 东
        }
        # 为相邻位置确定优先顺序
        adjacent: list[tuple[int, int]] = []
        for order in direction_orders:
            adjacent.append(adjacent_squares[order])

        for r, c in adjacent:
            if (
                0 <= r < self.height
                and 0 <= c < self.width
                and self.planet[r][c] is None
            ):
                # 将实体移至相邻空方格
                self.planet[r][c] = entity
                self.planet[row][col] = None
                entity.coords = (r, c)
                break

        # (2.) 检查能否在原方格中繁殖
        if coords != entity.coords and entity.remaining_reproduction_time <= 0:
            # 检查星球上的实体数是否小于上限
            if len(self.get_entities()) < MAX_ENTITIES:
                # 在原方格中繁殖
                self.planet[row][col] = Entity(prey=entity.prey, coords=coords)
                entity.reset_reproduction_time()
        else:
            entity.remaining_reproduction_time -= 1

    def perform_prey_actions(
        self, entity: Entity, direction_orders: list[Literal["N", "E", "S", "W"]]
    ) -> None:
        """
        执行猎物实体的行为。

        猎物遵循以下规则：
            1. 每个时元，猎物随机移动到一个相邻空方格。如果没有空方格，
               则不发生移动。
            2. 猎物存活一定时元后可以繁殖。它移动到相邻方格时，
               会在原位置留下新的猎物，同时重置繁殖时间。

        >>> wt = WaTor(WIDTH, HEIGHT)
        >>> reproducable_entity = Entity(True, coords=(0, 1))
        >>> reproducable_entity.remaining_reproduction_time = 0
        >>> wt.planet = [[None, reproducable_entity]]
        >>> wt.perform_prey_actions(reproducable_entity,
        ... direction_orders=["N", "W", "S", "E"])
        >>> wt.planet  # doctest: +NORMALIZE_WHITESPACE
        [[Entity(prey=True, coords=(0, 0), remaining_reproduction_time=5),
        Entity(prey=True, coords=(0, 1), remaining_reproduction_time=5)]]
        """
        self.move_and_reproduce(entity, direction_orders)

    def perform_predator_actions(
        self,
        entity: Entity,
        occupied_by_prey_coords: tuple[int, int] | None,
        direction_orders: list[Literal["N", "E", "S", "W"]],
    ) -> None:
        """
        执行捕食者实体的行为。

        :param occupied_by_prey_coords: 如果此位置有猎物，则移动到这里

        捕食者遵循以下规则：
            1. 每个时元，捕食者随机移动到一个被猎物占据的相邻方格。如果没有，
               则随机移动到相邻空方格；如果没有空方格，则不发生移动。
            2. 每个时元，每个捕食者损失一个单位的能量。
            3. 能量降至零时，捕食者死亡。
            4. 捕食者移动到被猎物占据的方格时，会吃掉猎物并获得一定能量。
            5. 捕食者存活一定时元后，可以采用与猎物完全相同的方式繁殖。

        >>> wt = WaTor(WIDTH, HEIGHT)
        >>> wt.set_planet([[Entity(True, coords=(0, 0)), Entity(False, coords=(0, 1))]])
        >>> wt.perform_predator_actions(Entity(False, coords=(0, 1)), (0, 0), [])
        >>> wt.planet  # doctest: +NORMALIZE_WHITESPACE
        [[Entity(prey=False, coords=(0, 0),
        remaining_reproduction_time=20, energy_value=19), None]]
        """
        assert entity.energy_value is not None  # [类型检查]

        # (3.) 实体能量为 0 时死亡
        if entity.energy_value == 0:
            self.planet[entity.coords[0]][entity.coords[1]] = None
            return

        # (1.) 如果可能，则移动到猎物所在位置
        if occupied_by_prey_coords is not None:
            # 杀死猎物
            prey = self.planet[occupied_by_prey_coords[0]][occupied_by_prey_coords[1]]
            assert prey is not None
            prey.alive = False

            # 移动到猎物所在位置
            self.planet[occupied_by_prey_coords[0]][occupied_by_prey_coords[1]] = entity
            self.planet[entity.coords[0]][entity.coords[1]] = None

            entity.coords = occupied_by_prey_coords
            # (4.) 吃掉猎物并获得能量
            entity.energy_value += PREDATOR_FOOD_VALUE
        else:
            # (5.) 如果已存活指定数量的时元，也会在此函数中繁殖
            self.move_and_reproduce(entity, direction_orders)

        # (2.) 每个时元，捕食者损失一个单位的能量
        entity.energy_value -= 1

    def run(self, *, iteration_count: int) -> None:
        """
        通过循环 `iteration_count` 次来模拟时间流逝。

        >>> wt = WaTor(WIDTH, HEIGHT)
        >>> wt.run(iteration_count=PREDATOR_INITIAL_ENERGY_VALUE - 1)
        >>> len(list(filter(lambda entity: entity.prey is False,
        ... wt.get_entities()))) >= PREDATOR_INITIAL_COUNT
        True
        """
        for iter_num in range(iteration_count):
            # 生成所有实体的列表，每次随机弹出一个实体以模拟真正的随机性，
            # 从而消除按宽度和高度依次遍历实体的系统化方式
            all_entities = self.get_entities()

            for __ in range(len(all_entities)):
                entity = all_entities.pop(randint(0, len(all_entities) - 1))
                if entity.alive is False:
                    continue

                directions: list[Literal["N", "E", "S", "W"]] = ["N", "E", "S", "W"]
                shuffle(directions)  # 随机打乱方向

                if entity.prey:
                    self.perform_prey_actions(entity, directions)
                else:
                    # 创建周围猎物的列表
                    surrounding_prey = self.get_surrounding_prey(entity)
                    surrounding_prey_coords = None

                    if surrounding_prey:
                        # 再次随机打乱顺序
                        shuffle(surrounding_prey)
                        surrounding_prey_coords = surrounding_prey[0].coords

                    self.perform_predator_actions(
                        entity, surrounding_prey_coords, directions
                    )

            # 平衡捕食者和猎物
            self.balance_predators_and_prey()

            if self.time_passed is not None:
                # 调用 time_passed 函数，在终端或图形中显示 Wa-Tor 星球。
                self.time_passed(self, iter_num)


def visualise(wt: WaTor, iter_number: int, *, colour: bool = True) -> None:
    """
    在终端中使用 ASCII 代码清屏，并按一定间隔重新打印 Wa-Tor 星球，
    从而直观显示其状态。

    使用 ASCII 颜色代码彩色显示捕食者和猎物：
        * (0x60f197) 猎物 = ``#``
        * (0xfffff) 捕食者 = ``x``

    >>> wt = WaTor(30, 30)
    >>> wt.set_planet([
    ... [Entity(True, coords=(0, 0)), Entity(False, coords=(0, 1)), None],
    ... [Entity(False, coords=(1, 0)), None, Entity(False, coords=(1, 2))],
    ... [None, Entity(True, coords=(2, 1)), None]
    ... ])
    >>> visualise(wt, 0, colour=False)  # doctest: +NORMALIZE_WHITESPACE
    #  x  .
    x  .  x
    .  #  .
    <BLANKLINE>
    Iteration: 0 | Prey count: 2 | Predator count: 3 |
    """
    if colour:
        __import__("os").system("")
        print("\x1b[0;0H\x1b[2J\x1b[?25l")

    reprint = "\x1b[0;0H" if colour else ""
    ansi_colour_end = "\x1b[0m " if colour else " "

    planet = wt.planet
    output = ""

    # 遍历星球中的每个实体
    for row in planet:
        for entity in row:
            if entity is None:
                output += " . "
            else:
                if colour is True:
                    output += (
                        "\x1b[38;2;96;241;151m"
                        if entity.prey
                        else "\x1b[38;2;255;255;15m"
                    )
                output += f" {'#' if entity.prey else 'x'}{ansi_colour_end}"

        output += "\n"

    entities = wt.get_entities()
    prey_count = sum(entity.prey for entity in entities)

    print(
        f"{output}\n Iteration: {iter_number} | Prey count: {prey_count} | "
        f"Predator count: {len(entities) - prey_count} | {reprint}"
    )
    # 阻塞线程，以便观察算法的可视化过程
    sleep(0.05)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    wt = WaTor(WIDTH, HEIGHT)
    wt.time_passed = visualise
    wt.run(iteration_count=100_000)
