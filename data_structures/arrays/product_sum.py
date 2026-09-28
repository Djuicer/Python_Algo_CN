"""
计算 乘积 和 从 Special 数组。
reference: https://dev.to/sfrasica/algorithms-product-sum-from-an-array-dc6

Python doctests 可以 为 运行 带有 following 命令：
python -m doctest -v product_sum.py

计算 乘积 和 的 "special" 数组 其 可以 包含 整数 或 嵌套
数组. 乘积 和 是 obtained 通过 添加 所有元素 并且 multiplying 通过 它们的
respective depths.

用于 示例，在 该数组 [x，y]，乘积 和 是 (x + y). 在 该数组 [x，[y，z]],
乘积 和 是 x + 2 * (y + z). 在 该数组 [x，[y，[z]]],
乘积 和 是 x + 2 * (y + 3z)。

示例 输入：
[5, 2, [-7, 1], 3, [6, [-13, 8], 4]]
输出: -12

"""

from timeit import timeit


def product_sum(arr: list[int | list], depth: int) -> int:
    """
    递归地 计算 乘积 和 的 一个数组。

    乘积 和 的 一个数组 是 定义 作为 和 的 其 元素 multiplied 通过
    它们的 respective depths.  如果 元素 是 一个列表，其 乘积 和 是 计算得出
    递归地 通过 multiplying 和 的 其 元素 带有 其 深度 plus 一个。

    参数：
        arr: 该数组 的 整数 并且 嵌套 列表。
        深度: 当前 深度 层级。

    返回值：
        int: 乘积 和 的数组。

    示例：
        >>> product_sum([1, 2, 3], 1)
        6
        >>> product_sum([-1, 2, [-3, 4]], 2)
        8
        >>> product_sum([1, 2, 3], -1)
        -6
        >>> product_sum([1, 2, 3], 0)
        0
        >>> product_sum([1, 2, 3], 7)
        42
        >>> product_sum((1, 2, 3), 7)
        42
        >>> product_sum({1, 2, 3}, 7)
        42
        >>> product_sum([1, -1], 1)
        0
        >>> product_sum([1, -2], 1)
        -1
        >>> product_sum([-3.5, [1, [0.5]]], 1)
        1.5

    """
    total_sum = 0
    for ele in arr:
        total_sum += product_sum(ele, depth + 1) if isinstance(ele, list) else ele
    return total_sum * depth


def product_sum_array(array: list[int | list]) -> int:
    """
    计算 乘积 和 的 一个数组。

    参数：
        数组 (列表[Union[int，列表]]): 该数组 的 整数 并且 嵌套 列表。

    返回值：
        int: 乘积 和 的数组。

    示例：
        >>> product_sum_array([1, 2, 3])
        6
        >>> product_sum_array([1, [2, 3]])
        11
        >>> product_sum_array([1, [2, [3, 4]]])
        47
        >>> product_sum_array([0])
        0
        >>> product_sum_array([-3.5, [1, [0.5]]])
        1.5
        >>> product_sum_array([1, -2])
        -1

    """
    return product_sum(array, 1)


def product_sum_iterative(arr: list[int | list]) -> int:
    """
    它 计算 乘积 和 的 一个数组 使用 迭代 方法。
    它's similar 到 BFS 算法 (Breadth 第一个 搜索 算法)。
    它's won't 运行 到 栈 overflow 作为 compared 到 recursion 方法

    参数：
        数组(列表[Union[int，列表]]): 该数组 的 整数/列表

    返回值：
        int: 乘积 和 的数组。

    Logic :
        1. 初始化 队列 其 存储 该列表，当前
            深度 并且 它's 乘法 因子
            eg. 队列 -> [(arr，深度，multiplication_factor)]

        2. 循环 until 队列 为空
            1. Take 前端 元素 从 队列 并且 弹出 它
            2. 迭代 在 前端 元素
                如果 当前元素 是 嵌套 列表
                    - 则 添加 该 到 队列 带有 updated 深度
                      并且 乘法 因子
                否则 如果 当前元素 是 不 嵌套
                    - 则 更新 乘积 和 变量 通过 multiplying
                      当前元素 带有 multiplicaton 因子

    算法 flow 示例 ->
        输入 列表 - [5，2，[-7，1]，3，[6，[-13，8]，4]]

        初始化 队列 - [([5，2，[-7，1]，3，[6，[-13，8]，4]]，1，1)]

        步骤 0
            队列 - [([5，2，[-7，1]，3，[6，[-13，8]，4]]，1，1)]
            队列 前端 元素 -
                列表 - [5，2，[-7，1]，3，[6，[-13，8]，4]]
                深度 - 1
                乘法 因子 - 1

            乘积 和 = 0 (上一个) + 5 * 1 + 2 * 1 + 3 * 1 = 10
        -------------------------------------------------------
        步骤 1
            队列 - [([-7，1]，2，2)，([6，[-13，8]，4]，2，2)]
            队列 前端 元素 -
                列表 - [-7，1]
                深度 - 2
                乘法 因子 - 2

            乘积 和 = 10 (上一个) +  (-7) * 2 + 1 * 2 = -2
        -------------------------------------------------------
        步骤 2
            队列 - [([6，[-13，8]，4]，2，2)]
            队列 前端 元素 -
                列表 - [6，[-13，8]，4]
                深度 - 2
                乘法 因子 - 2

            乘积 和 = -2 (上一个) + 6 * 2 +  4 * 2 = 18
        -------------------------------------------------------
        步骤 3
            队列 - [([-13，8]，3，6)]
            队列 前端 元素 -
                列表 - [-13，8]
                深度 - 3
                乘法 因子 - 6

            乘积 和 = 18 (上一个) + (-13) * 6 + 8 * 6 = -12
        -------------------------------------------------------

    示例：
        >>> product_sum_array([1, 2, 3])
        6
        >>> product_sum_array([1, [2, 3]])
        11
        >>> product_sum_array([1, [2, [3, 4]]])
        47
        >>> product_sum_array([0])
        0
        >>> product_sum_array([-3.5, [1, [0.5]]])
        1.5
        >>> product_sum_array([1, -2])
        -1
    """

    # 初始化 队列 带有 深度 并且 乘法 因子
    queue = [(arr, 1, 1)]

    product_sum = 0

    while queue:
        queue_front_list, depth, multiplication_factor = queue.pop(0)

        for element in queue_front_list:
            if isinstance(element, list):
                queue.append((element, depth + 1, multiplication_factor * (depth + 1)))
            else:
                product_sum += element * multiplication_factor

    return product_sum


def benchmark() -> None:
    """
    Benchmark 代码 comparing 不同 version。
    """

    setup = "from __main__ import product_sum_array, product_sum_iterative"

    print(
        timeit("product_sum_array([5, 2, [-7, 1], 3, [6, [-13, 8], 4]])", setup=setup)
    )
    # 1.1448657000437379

    print(
        timeit(
            "product_sum_iterative([5, 2, [-7, 1], 3, [6, [-13, 8], 4]])", setup=setup
        )
    )
    # 1.6824490998405963


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
