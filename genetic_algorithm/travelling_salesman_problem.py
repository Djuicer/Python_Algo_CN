"""
使用遗传算法求解旅行商问题（Travelling Salesman Problem，TSP）。该问题要求：
“给定一组城市及每对城市间的距离，访问每座城市恰好一次并返回出发城市的
最短路线是什么？”

https://en.wikipedia.org/wiki/Genetic_algorithm
https://en.wikipedia.org/wiki/Travelling_salesman_problem

Author: Clark
"""

import copy
import random

cities = {
    0: [0, 0],
    1: [0, 5],
    2: [3, 8],
    3: [8, 10],
    4: [12, 8],
    5: [12, 4],
    6: [8, 0],
    7: [6, 2],
}


def main(
    cities: dict[int, list[int]],
    population_size: int,
    iterations_num: int,
    crossover_probability: float,
    mutation_probability: float,
) -> tuple[list[int], float]:
    """
    遗传算法主函数。

    该算法具有随机性，因此应为 ``random`` 设置种子，并断言返回路线的不变量，
    而不是断言某个精确顺序（不同平台或 Python 版本之间无法复现该顺序）。

    >>> import random
    >>> random.seed(0)
    >>> path, best = main(cities=cities, population_size=100, iterations_num=100,
    ...     crossover_probability=0.6, mutation_probability=0.2)
    >>> path[0] == 0 and path[-1] == 0  # starts and ends at the origin city
    True
    >>> sorted(path[:-1]) == sorted(cities)  # every city visited exactly once
    True
    >>> 37 <= best < 45  # converges close to the optimal round-trip (~37.9)
    True
    >>> main(cities={0: [0, 0], 1: [2, 2]}, population_size=10, iterations_num=10,
    ...     crossover_probability=0.6, mutation_probability=0.2)
    ([0, 1, 0], 5.656854249492381)
    >>> main(cities={},population_size=10,iterations_num=10,
    ... crossover_probability=0.6,mutation_probability=0.2)
    Traceback (most recent call last):
      ...
    IndexError: list assignment index out of range
    """
    best_path: list[int] = []
    best_distance = float("inf")

    chromosomes, cities_list = init(cities, population_size)
    fitness_matrix, best_path, best_distance = fitness(
        cities, chromosomes, best_path, best_distance
    )
    for _ in range(iterations_num):
        """
        取消注释以选择另一种选择算子。
        两种选择算子同一时间只能取消其中一种的注释。
        """
        # chromosomes = chose_ts(fitness_matrix, chromosomes, population_size)
        chromosomes = chose_rws(fitness_matrix, chromosomes, population_size)
        for x in range(int(population_size / 2)):  # 种群交叉
            chromosomes[x], chromosomes[x + int(population_size / 2)] = crossing(
                chromosomes[x],
                chromosomes[x + int(population_size / 2)],
                crossover_probability,
                cities_list,
            )
        for x in range(population_size):  # 种群变异
            chromosomes[x] = mutate(chromosomes[x], mutation_probability)

        fitness_matrix, best_path, best_distance = fitness(
            cities, chromosomes, best_path, best_distance
        )

    return best_path, best_distance


def distance(city1: list[int], city2: list[int]) -> float:
    """
    计算两个坐标点之间的距离。
    >>> distance([0, 0], [3, 4] )
    5.0
    >>> distance([0, 0], [-3, 4] )
    5.0
    >>> distance([0, 0], [-3, -4] )
    5.0
    """
    return (((city1[0] - city2[0]) ** 2) + ((city1[1] - city2[1]) ** 2)) ** 0.5


def init(
    cities: dict[int, list[int]], population_size: int
) -> tuple[list[list[int]], list[int]]:
    """
    初始化并生成初始种群。
    >>> init(cities={0: [0, 0], 1: [2, 2]}, population_size=2)
    ([[0, 1, 0], [0, 1, 0]], [1])
    >>> init(cities={0: [0, 0], 1: [2, 2]}, population_size=0)
    ([], [1])
    >>> init(cities={},population_size=2)
    Traceback (most recent call last):
    ...
    IndexError: list assignment index out of range
    """
    chromosomes = []
    cities_list = list(cities.keys())
    del cities_list[0]
    for _ in range(population_size):
        chromosome = []
        chromosome.append(0)  # 添加起点
        chromosome.extend(random.sample(cities_list, len(cities_list)))
        chromosome.append(0)  # 添加终点
        chromosomes.append(chromosome)
    return chromosomes, cities_list


def fitness(
    cities: dict[int, list[int]],
    chromosomes: list[list[int]],
    best_path: list[int],
    best_distance: float,
) -> tuple[list[float], list[int], float]:
    """
    计算种群适应度。
    生成适应度矩阵，并获得当前种群中的最优值。
    >>> fitness(cities={0: [0, 0], 1: [2, 2]},chromosomes=[[0,1,0]],
    ... best_path=[], best_distance=float("inf"))
    ([0.17677669529663687], [0, 1, 0], 5.656854249492381)
    >>> fitness(cities={0: [0, 0], 1: [2, 2]},chromosomes=[[0,1,0],[0,1,0]],
    ... best_path=[], best_distance=float("inf"))
    ([0.17677669529663687, 0.17677669529663687], [0, 1, 0], 5.656854249492381)
    >>> fitness(cities={}, chromosomes=[[0,1,0]],
    ... best_path=[], best_distance=float("inf"))
    Traceback (most recent call last):
    ...
    KeyError: 0
    >>> fitness(cities={0: [0, 0], 1: [2, 2]},chromosomes=[],
    ... best_path=[], best_distance=float("inf"))
    ([], [], inf)
    """
    fitness_matrix = []
    new_best_path = best_path
    new_best_distance = best_distance
    for chromosome in chromosomes:
        total_distance = 0.0
        for i in range(len(chromosome) - 1):  # 计算总距离
            total_distance += distance(cities[chromosome[i]], cities[chromosome[i + 1]])
        fitness_matrix.append(1 / total_distance)
        if total_distance < new_best_distance:
            new_best_path = chromosome
            new_best_distance = total_distance

    return fitness_matrix, new_best_path, new_best_distance


def chose_ts(
    fitness_matrix: list[float], chromosomes: list[list[int]], population_size: int
) -> list[list[int]]:
    """
    一种选择算子：锦标赛选择（Tournament Selection）。
    >>> chose_ts(fitness_matrix=[1], chromosomes=[[0,1,0]], population_size=1)
    [[0, 1, 0]]
    >>> chose_ts(fitness_matrix=[1], chromosomes=[0,1,0], population_size=0)
    []
    >>> chose_ts(fitness_matrix=[], chromosomes=[[0,1,0]], population_size=1)
    Traceback (most recent call last):
    ...
    IndexError: list index out of range
    >>> chose_ts(fitness_matrix=[1], chromosomes=[], population_size=1)
    Traceback (most recent call last):
    ...
    IndexError: list index out of range
    >>> import random
    >>> random.seed(0)
    >>> chose_ts(fitness_matrix=[1], chromosomes=[0, 1, 0], population_size=2)
    Traceback (most recent call last):
    ...
    IndexError: list index out of range
    """
    chromosomes_new = []
    for _ in range(population_size):
        x1 = random.randint(0, population_size - 1)
        x2 = random.randint(0, population_size - 1)
        if fitness_matrix[x1] >= fitness_matrix[x2]:
            chromosomes_new.append(chromosomes[x1])
        else:
            chromosomes_new.append(chromosomes[x2])
    return chromosomes_new


def chose_rws(
    fitness_matrix: list[float], chromosomes: list[list[int]], population_size: int
) -> list[list[int]]:
    """
    一种选择算子：轮盘赌选择（Roulette Wheel Selection）。
    >>> chose_rws(fitness_matrix=[1], chromosomes=[[0,1,0]], population_size=1)
    [[0, 1, 0]]
    >>> chose_rws(fitness_matrix=[1], chromosomes=[0,1,0], population_size=0)
    [0, 1, 0]
    >>> chose_rws(fitness_matrix=[], chromosomes=[[0,1,0]], population_size=1)
    Traceback (most recent call last):
    ...
    IndexError: list index out of range
    >>> chose_rws(fitness_matrix=[1], chromosomes=[], population_size=1)
    Traceback (most recent call last):
    ...
    IndexError: list index out of range
    >>> chose_rws(fitness_matrix=[1], chromosomes=[0,1,0], population_size=2)
    [0, 0, 0]
    """
    probabilitys = [0.0] * len(fitness_matrix)
    total_probability = 0.0
    for i in fitness_matrix:
        total_probability += i
    for i in range(len(fitness_matrix)):
        probabilitys[i] = fitness_matrix[i] / total_probability

    chromosomes_new = copy.deepcopy(chromosomes)
    for i in range(population_size):
        k = 0.0
        r = random.uniform(0, 1)
        for j in range(population_size):
            k = k + probabilitys[j]
            if r <= k:
                chromosomes_new[i] = chromosomes[j]
                break
    return chromosomes_new


def crossing(
    chromosome_a: list[int],
    chromosome_b: list[int],
    crossover_probability: float,
    cities_list: list[int],
) -> tuple[list[int], list[int]]:
    """
    种群交叉。
    >>> crossing(chromosome_a=[0,1,0], chromosome_b=[0,1,0],
    ... crossover_probability=0,cities_list=[1])
    ([0, 1, 0], [0, 1, 0])
    >>> crossing(chromosome_a=[0,1,0], chromosome_b=[0,1,0],
    ... crossover_probability=1,cities_list=[1])
    ([0, 1, 0], [0, 1, 0])
    >>> crossing(chromosome_a=[0,1,0], chromosome_b=[],
    ... crossover_probability=1,cities_list=[1])
    Traceback (most recent call last):
    ...
    IndexError: list index out of range
    >>> crossing(chromosome_a=[0,1,0], chromosome_b=[0,1,0],
    ... crossover_probability=1,cities_list=[])
    ([0, 1, 0], [0, 1, 0])
    """
    new_chromosome_a = copy.deepcopy(chromosome_a)
    new_chromosome_b = copy.deepcopy(chromosome_b)

    if random.random() <= crossover_probability:
        crossover_segment = sorted(
            [
                random.randint(0, len(new_chromosome_a) - 1),
                random.randint(0, len(new_chromosome_a) - 1),
            ]
        )

        for k in range((crossover_segment[1] - crossover_segment[0]) + 1):
            (
                new_chromosome_a[crossover_segment[0] + k],
                new_chromosome_b[crossover_segment[0] + k],
            ) = (
                new_chromosome_b[crossover_segment[0] + k],
                new_chromosome_a[crossover_segment[0] + k],
            )

        for chromosome in [new_chromosome_a, new_chromosome_b]:
            unique_elements_set = set(chromosome)
            if len(unique_elements_set) != len(
                chromosome
            ):  # 判断染色体片段中是否存在重复
                for segment_index in range(
                    (crossover_segment[1] - crossover_segment[0]) + 1
                ):
                    target_index = 0
                    for chrom_index in range(
                        1, len(chromosome) - 1
                    ):  # 搜索时排除起点和终点 0
                        if chrom_index == (crossover_segment[0] + segment_index):
                            continue
                        if (
                            chromosome[chrom_index]
                            == chromosome[crossover_segment[0] + segment_index]
                        ):
                            target_index = chrom_index
                            break
                    if target_index != 0:
                        cities_list_copy = copy.deepcopy(cities_list)
                        for t in chromosome:
                            try:
                                cities_list_copy.remove(t)
                            except ValueError:
                                continue
                        chromosome[target_index] = random.sample(cities_list_copy, 1)[0]

    return new_chromosome_a, new_chromosome_b


def mutate(chromosome: list[int], mutation_probability: float) -> list[int]:
    """
    种群变异：交换内部的两座城市（两个端点仍为 0）。

    >>> mutate([0, 1, 0], mutation_probability=0)  # no mutation -> unchanged
    [0, 1, 0]
    >>> import random
    >>> random.seed(1)
    >>> mutate([0, 1, 2, 3, 0], mutation_probability=1)  # swaps two interior cities
    [0, 2, 1, 3, 0]

    空染色体没有可交换的内部城市；由于标准库的确切异常消息会随 Python 版本
    变化，因此只匹配异常类型。

    >>> mutate([], mutation_probability=1)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError
    """
    new_chromosome = copy.deepcopy(chromosome)
    if random.random() <= mutation_probability:
        mutate_location = [
            random.randint(1, len(new_chromosome) - 2),
            random.randint(1, len(new_chromosome) - 2),
        ]  # 排除起点和终点 0
        new_chromosome[mutate_location[0]], new_chromosome[mutate_location[1]] = (
            new_chromosome[mutate_location[1]],
            new_chromosome[mutate_location[0]],
        )
    return new_chromosome


if __name__ == "__main__":
    best_path, best_distance = main(
        cities=cities,
        population_size=100,
        iterations_num=100,
        crossover_probability=0.6,
        mutation_probability=0.2,
    )

    print(f"{best_path = }")
    print(f"{best_distance = }")
