# https://en.wikipedia.org/wiki/Simulated_annealing
import math
import random
from typing import Any

from .hill_climbing import SearchProblem


def simulated_annealing(
    search_prob,
    find_max: bool = True,
    max_x: float = math.inf,
    min_x: float = -math.inf,
    max_y: float = math.inf,
    min_y: float = -math.inf,
    visualization: bool = False,
    start_temperate: float = 100,
    rate_of_decrease: float = 0.01,
    threshold_temp: float = 1,
) -> Any:
    """
    模拟退火（Simulated Annealing）算法的实现。从给定状态出发，
    找出所有邻居。随机选择一个邻居，如果它能改进
    解，就移向该邻居；如果它不能改进解，
    则生成一个 0 到 1 之间的随机实数，若该数位于特定
    范围内（根据温度计算），就移向该邻居，否则
    重新随机选择邻居并重复此过程。

    Args:
        search_prob: 初始搜索状态。
        find_max: If True, the algorithm should find the minimum else the minimum.
        max_x, min_x, max_y, min_y: x 和 y 的上下界。
        visualization: 为 True 时显示 matplotlib 图形。
        start_temperate: 程序启动时系统的初始温度。
        rate_of_decrease: 每次迭代中温度的下降比例。
        threshold_temp: 温度阈值，低于此值时结束搜索
    返回具有最大（或最小）得分的搜索状态。
    """
    search_end = False
    current_state = search_prob
    current_temp = start_temperate
    scores = []
    iterations = 0
    best_state = None

    while not search_end:
        current_score = current_state.score()
        if best_state is None or current_score > best_state.score():
            best_state = current_state
        scores.append(current_score)
        iterations += 1
        next_state = None
        neighbors = current_state.get_neighbors()
        while (
            next_state is None and neighbors
        ):  # 继续寻找可以移向的邻居
            index = random.randint(0, len(neighbors) - 1)  # 随机选择一个邻居
            picked_neighbor = neighbors.pop(index)
            change = picked_neighbor.score() - current_score

            if (
                picked_neighbor.x > max_x
                or picked_neighbor.x < min_x
                or picked_neighbor.y > max_y
                or picked_neighbor.y < min_y
            ):
                continue  # 邻居超出边界

            if not find_max:
                change = change * -1  # 寻找最小值时反转变化量的符号
            if change > 0:  # 能够改进解
                next_state = picked_neighbor
            else:
                probability = (math.e) ** (
                    change / current_temp
                )  # 概率计算函数
                if random.random() < probability:  # 随机数小于接受概率
                    next_state = picked_neighbor
        current_temp = current_temp - (current_temp * rate_of_decrease)

        if current_temp < threshold_temp or next_state is None:
            # 温度低于阈值，或未找到合适的邻居
            search_end = True
        else:
            current_state = next_state

    if visualization:
        from matplotlib import pyplot as plt

        plt.plot(range(iterations), scores)
        plt.xlabel("Iterations")
        plt.ylabel("Function values")
        plt.show()
    return best_state


if __name__ == "__main__":

    def test_f1(x, y):
        return (x**2) + (y**2)

    # 以初始坐标 (12, 47) 开始搜索
    prob = SearchProblem(x=12, y=47, step_size=1, function_to_optimize=test_f1)
    local_min = simulated_annealing(
        prob, find_max=False, max_x=100, min_x=5, max_y=50, min_y=-5, visualization=True
    )
    print(
        "The minimum score for f(x, y) = x^2 + y^2 with the domain 100 > x > 5 "
        f"and 50 > y > - 5 found via hill climbing: {local_min.score()}"
    )

    # 以初始坐标 (12, 47) 开始搜索
    prob = SearchProblem(x=12, y=47, step_size=1, function_to_optimize=test_f1)
    local_min = simulated_annealing(
        prob, find_max=True, max_x=100, min_x=5, max_y=50, min_y=-5, visualization=True
    )
    print(
        "The maximum score for f(x, y) = x^2 + y^2 with the domain 100 > x > 5 "
        f"and 50 > y > - 5 found via hill climbing: {local_min.score()}"
    )

    def test_f2(x, y):
        return (3 * x**2) - (6 * y)

    prob = SearchProblem(x=3, y=4, step_size=1, function_to_optimize=test_f1)
    local_min = simulated_annealing(prob, find_max=False, visualization=True)
    print(
        "The minimum score for f(x, y) = 3*x^2 - 6*y found via hill climbing: "
        f"{local_min.score()}"
    )

    prob = SearchProblem(x=3, y=4, step_size=1, function_to_optimize=test_f1)
    local_min = simulated_annealing(prob, find_max=True, visualization=True)
    print(
        "The maximum score for f(x, y) = 3*x^2 - 6*y found via hill climbing: "
        f"{local_min.score()}"
    )
