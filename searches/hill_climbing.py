# https://en.wikipedia.org/wiki/Hill_climbing
import math
from collections.abc import Callable


class SearchProblem:
    """
    用于定义搜索问题的接口。
    下面以数学函数为例说明该接口。
    """

    def __init__(
        self,
        x: int,
        y: int,
        step_size: int,
        function_to_optimize: Callable[[int, int], int | float],
    ) -> None:
        """
        搜索问题的构造函数。

        x: 当前搜索状态的 x 坐标。
        y: 当前搜索状态的 y 坐标。
        step_size: 查找邻居时的步长。
        function_to_optimize: 待优化的函数，签名为 f(x, y)。
        """
        self.x = x
        self.y = y
        self.step_size = step_size
        self.function = function_to_optimize

    def score(self) -> int | float:
        """
        返回以当前 x 和 y 坐标调用函数所得的结果。
        >>> def test_function(x, y):
        ...     return x + y
        >>> SearchProblem(0, 0, 1, test_function).score()  # 0 + 0 = 0
        0
        >>> SearchProblem(5, 7, 1, test_function).score()  # 5 + 7 = 12
        12
        """
        return self.function(self.x, self.y)

    def get_neighbors(self) -> list["SearchProblem"]:
        """
        返回与当前坐标相邻的邻居坐标列表。

        邻居：
        | 0 | 1 | 2 |
        | 3 | _ | 4 |
        | 5 | 6 | 7 |
        """
        step_size = self.step_size
        return [
            SearchProblem(x, y, step_size, self.function)
            for x, y in (
                (self.x - step_size, self.y - step_size),
                (self.x - step_size, self.y),
                (self.x - step_size, self.y + step_size),
                (self.x, self.y - step_size),
                (self.x, self.y + step_size),
                (self.x + step_size, self.y - step_size),
                (self.x + step_size, self.y),
                (self.x + step_size, self.y + step_size),
            )
        ]

    def __hash__(self) -> int:
        """
        对当前搜索状态的字符串表示计算哈希值。
        """
        return hash(str(self))

    def __eq__(self, obj: object) -> bool:
        """
        检查两个对象是否相等。
        """
        if isinstance(obj, SearchProblem):
            return hash(str(self)) == hash(str(obj))
        return False

    def __str__(self) -> str:
        """
        当前搜索状态的字符串表示。
        >>> str(SearchProblem(0, 0, 1, None))
        'x: 0 y: 0'
        >>> str(SearchProblem(2, 5, 1, None))
        'x: 2 y: 5'
        """
        return f"x: {self.x} y: {self.y}"


def hill_climbing(
    search_prob: SearchProblem,
    find_max: bool = True,
    max_x: float = math.inf,
    min_x: float = -math.inf,
    max_y: float = math.inf,
    min_y: float = -math.inf,
    visualization: bool = False,
    max_iter: int = 10000,
) -> SearchProblem:
    """
    爬山算法（Hill Climbing）的实现。
    从给定状态出发，找出所有邻居，
    移向能带来最大（或最小）变化的邻居。
    不断重复此过程，直到当前状态下
    没有能够改进解的邻居。
        Args:
            search_prob: 初始搜索状态。
            find_max: 为 True 时寻找最大值，否则寻找最小值。
            max_x, min_x, max_y, min_y: x 和 y 的上下界。
            visualization: 为 True 时显示 matplotlib 图形。
            max_iter: 迭代次数。
        返回具有最大（或最小）得分的搜索状态。
    """
    current_state = search_prob
    scores = []  # 用于保存每次迭代当前得分的列表
    iterations = 0
    solution_found = False
    visited = set()
    while not solution_found and iterations < max_iter:
        visited.add(current_state)
        iterations += 1
        current_score = current_state.score()
        scores.append(current_score)
        neighbors = current_state.get_neighbors()
        max_change = -math.inf
        min_change = math.inf
        next_state = None  # 用于保存下一步的最佳邻居
        for neighbor in neighbors:
            if neighbor in visited:
                continue  # 避免重复访问同一状态
            if (
                neighbor.x > max_x
                or neighbor.x < min_x
                or neighbor.y > max_y
                or neighbor.y < min_y
            ):
                continue  # 邻居超出边界
            change = neighbor.score() - current_score
            if find_max:  # 寻找最大值
                # 朝上升幅度最大的方向移动
                if change > max_change and change > 0:
                    max_change = change
                    next_state = neighbor
            elif change < min_change and change < 0:  # 寻找最小值
                # 朝下降幅度最大的方向移动
                min_change = change
                next_state = neighbor
        if next_state is not None:
            # 找到了至少一个能改进当前状态的邻居
            current_state = next_state
        else:
            # 没有能改进解的邻居，因此停止搜索
            solution_found = True

    if visualization:
        from matplotlib import pyplot as plt

        plt.plot(range(iterations), scores)
        plt.xlabel("Iterations")
        plt.ylabel("Function values")
        plt.show()

    return current_state


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    def test_f1(x, y):
        return (x**2) + (y**2)

    # 以初始坐标 (3, 4) 开始搜索
    prob = SearchProblem(x=3, y=4, step_size=1, function_to_optimize=test_f1)
    local_min = hill_climbing(prob, find_max=False)
    print(
        "The minimum score for f(x, y) = x^2 + y^2 found via hill climbing: "
        f"{local_min.score()}"
    )

    # 以初始坐标 (12, 47) 开始搜索
    prob = SearchProblem(x=12, y=47, step_size=1, function_to_optimize=test_f1)
    local_min = hill_climbing(
        prob, find_max=False, max_x=100, min_x=5, max_y=50, min_y=-5, visualization=True
    )
    print(
        "The minimum score for f(x, y) = x^2 + y^2 with the domain 100 > x > 5 "
        f"and 50 > y > - 5 found via hill climbing: {local_min.score()}"
    )

    def test_f2(x, y):
        return (3 * x**2) - (6 * y)

    prob = SearchProblem(x=3, y=4, step_size=1, function_to_optimize=test_f1)
    local_min = hill_climbing(prob, find_max=True)
    print(
        "The maximum score for f(x, y) = x^2 + y^2 found via hill climbing: "
        f"{local_min.score()}"
    )
