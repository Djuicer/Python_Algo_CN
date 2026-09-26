"""
用于求解旅行商问题（Travelling Salesman Problem）的禁忌搜索（Tabu Search）
算法纯 Python 实现，其中城市间的距离是对称的（即城市
'a' 到城市 'b' 的距离与城市 'b' 到城市 'a' 的距离相同）。
TSP 可以用图表示。城市对应节点，
城市间的距离对应节点间边的权重。

存储图的 .txt 文件格式如下：

node1 node2 distance_between_node1_and_node2
node1 node3 distance_between_node1_and_node3
...

注意，node1、node2 及它们之间的距离只能出现一次。也就是说，
.txt 文件中不应同时存在：
node1 node2 distance_between_node1_and_node2
node2 node1 distance_between_node2_and_node1

运行 pytest 请使用以下命令：
pytest

手动测试请运行：
python tabu_search.py -f your_file_name.txt -number_of_iterations_of_tabu_search \
    -s size_of_tabu_search
例如：python tabu_search.py -f tabudata2.txt -i 4 -s 3
"""

import argparse
import copy


def generate_neighbours(path):
    """
    根据包含图数据的文件路径，生成记录邻居及
    到各邻居代价的字典。

    :param path: 包含图数据的 .txt 文件路径（例如 tabudata2.txt）
    :return dict_of_neighbours: 字典，以各节点为键，以列表的列表为值，
        记录该节点的邻居及到各邻居的代价（距离）。

    dict_of_neighbours 示例：
    >>) dict_of_neighbours[a]
    [[b,20],[c,18],[d,22],[e,26]]

    这里表示节点（城市）'a' 的邻居：节点 'b'
    距离为 20，节点 'c' 距离为 18，节点 'd' 距离为 22，
    节点 'e' 距离为 26。
    """

    dict_of_neighbours = {}

    with open(path) as f:
        for line in f:
            if line.split()[0] not in dict_of_neighbours:
                _list = []
                _list.append([line.split()[1], line.split()[2]])
                dict_of_neighbours[line.split()[0]] = _list
            else:
                dict_of_neighbours[line.split()[0]].append(
                    [line.split()[1], line.split()[2]]
                )
            if line.split()[1] not in dict_of_neighbours:
                _list = []
                _list.append([line.split()[0], line.split()[2]])
                dict_of_neighbours[line.split()[1]] = _list
            else:
                dict_of_neighbours[line.split()[1]].append(
                    [line.split()[0], line.split()[2]]
                )

    return dict_of_neighbours


def generate_first_solution(path, dict_of_neighbours):
    """
    为禁忌搜索生成初始解，
    采用 redundant resolution strategy。即从起始
    节点（例如节点 'a'）出发，前往距离它最近的城市
    （假设为节点 'c'），再前往距离节点 'c' 最近的城市，依此类推，
    直到访问所有城市并返回起始节点。

    :param path: 包含图数据的 .txt 文件路径（例如 tabudata2.txt）
    :param dict_of_neighbours: 字典，以各节点为键，以列表的列表为值，
        记录该节点的邻居及到各邻居的代价（距离）。
    :return first_solution: 禁忌搜索首次迭代使用的解，以列表表示，
        由 redundant resolution strategy 生成。
    :return distance_of_first_solution: 旅行商沿 first_solution 中的路径
        行进时的总距离。
    """

    with open(path) as f:
        start_node = f.read(1)
    end_node = start_node

    first_solution = []

    visiting = start_node

    distance_of_first_solution = 0
    while visiting not in first_solution:
        minim = 10000
        for k in dict_of_neighbours[visiting]:
            if int(k[1]) < int(minim) and k[0] not in first_solution:
                minim = k[1]
                best_node = k[0]

        first_solution.append(visiting)
        distance_of_first_solution = distance_of_first_solution + int(minim)
        visiting = best_node

    first_solution.append(end_node)

    position = 0
    for k in dict_of_neighbours[first_solution[-2]]:
        if k[0] == start_node:
            break
        position += 1

    distance_of_first_solution = (
        distance_of_first_solution
        + int(dict_of_neighbours[first_solution[-2]][position][1])
        - 10000
    )
    return first_solution, distance_of_first_solution


def find_neighborhood(solution, dict_of_neighbours):
    """
    使用 1-1 交换方法生成某个解的邻域（Neighborhood），并按
    各解的总距离从小到大排序。具体来说，
    将解中的每个节点分别与其他节点交换，
    所生成的一组解称为邻域。

    :param solution: 待求邻域的解。
    :param dict_of_neighbours: 字典，以各节点为键，以列表的列表为值，
        记录该节点的邻居及到各邻居的代价（距离）。
    :return neighborhood_of_solution: 一个列表，包含由输入解
        通过 1-1 交换生成的各个解及其总距离，
        其中每个解及其距离也以列表表示

    示例：
    >>> find_neighborhood(['a', 'c', 'b', 'd', 'e', 'a'],
    ...                   {'a': [['b', '20'], ['c', '18'], ['d', '22'], ['e', '26']],
    ...                    'c': [['a', '18'], ['b', '10'], ['d', '23'], ['e', '24']],
    ...                    'b': [['a', '20'], ['c', '10'], ['d', '11'], ['e', '12']],
    ...                    'e': [['a', '26'], ['b', '12'], ['c', '24'], ['d', '40']],
    ...                    'd': [['a', '22'], ['b', '11'], ['c', '23'], ['e', '40']]}
    ...                   )  # doctest: +NORMALIZE_WHITESPACE
    [['a', 'e', 'b', 'd', 'c', 'a', 90],
     ['a', 'c', 'd', 'b', 'e', 'a', 90],
     ['a', 'd', 'b', 'c', 'e', 'a', 93],
     ['a', 'c', 'b', 'e', 'd', 'a', 102],
     ['a', 'c', 'e', 'd', 'b', 'a', 113],
     ['a', 'b', 'c', 'd', 'e', 'a', 119]]
    """

    neighborhood_of_solution = []

    for n in solution[1:-1]:
        idx1 = solution.index(n)
        for kn in solution[1:-1]:
            idx2 = solution.index(kn)
            if n == kn:
                continue

            _tmp = copy.deepcopy(solution)
            _tmp[idx1] = kn
            _tmp[idx2] = n

            distance = 0

            for k in _tmp[:-1]:
                next_node = _tmp[_tmp.index(k) + 1]
                for i in dict_of_neighbours[k]:
                    if i[0] == next_node:
                        distance = distance + int(i[1])
            _tmp.append(distance)

            if _tmp not in neighborhood_of_solution:
                neighborhood_of_solution.append(_tmp)

    index_of_last_item_in_the_list = len(neighborhood_of_solution[0]) - 1

    neighborhood_of_solution.sort(key=lambda x: x[index_of_last_item_in_the_list])
    return neighborhood_of_solution


def tabu_search(
    first_solution, distance_of_first_solution, dict_of_neighbours, iters, size
):
    """
    用于求解旅行商问题的禁忌搜索算法
    纯 Python 实现。

    :param first_solution: 禁忌搜索首次迭代使用的解，以列表表示，
        由 redundant resolution strategy 生成。
    :param distance_of_first_solution: 旅行商沿 first_solution 中的路径
        行进时的总距离。
    :param dict_of_neighbours: 字典，以各节点为键，以列表的列表为值，
        记录该节点的邻居及到各邻居的代价（距离）。
    :param iters: 禁忌搜索执行的迭代次数。
    :param size: 禁忌表的大小。
    :return best_solution_ever: 禁忌搜索执行过程中
        出现的总距离最小的解。
    :return best_cost: 旅行商沿 best_solution_ever 中的路径
        行进时的总距离。
    """
    count = 1
    solution = first_solution
    tabu_list = []
    best_cost = distance_of_first_solution
    best_solution_ever = solution

    while count <= iters:
        neighborhood = find_neighborhood(solution, dict_of_neighbours)
        index_of_best_solution = 0
        best_solution = neighborhood[index_of_best_solution]
        best_cost_index = len(best_solution) - 1

        found = False
        while not found:
            i = 0
            while i < len(best_solution):
                if best_solution[i] != solution[i]:
                    first_exchange_node = best_solution[i]
                    second_exchange_node = solution[i]
                    break
                i = i + 1

            if [first_exchange_node, second_exchange_node] not in tabu_list and [
                second_exchange_node,
                first_exchange_node,
            ] not in tabu_list:
                tabu_list.append([first_exchange_node, second_exchange_node])
                found = True
                solution = best_solution[:-1]
                cost = neighborhood[index_of_best_solution][best_cost_index]
                if cost < best_cost:
                    best_cost = cost
                    best_solution_ever = solution
            else:
                index_of_best_solution = index_of_best_solution + 1
                best_solution = neighborhood[index_of_best_solution]

        if len(tabu_list) >= size:
            tabu_list.pop(0)

        count = count + 1

    return best_solution_ever, best_cost


def main(args=None) -> None:
    dict_of_neighbours = generate_neighbours(args.File)

    first_solution, distance_of_first_solution = generate_first_solution(
        args.File, dict_of_neighbours
    )

    best_sol, best_cost = tabu_search(
        first_solution,
        distance_of_first_solution,
        dict_of_neighbours,
        args.Iterations,
        args.Size,
    )

    print(f"Best solution: {best_sol}, with total distance: {best_cost}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tabu Search")
    parser.add_argument(
        "-f",
        "--File",
        type=str,
        help="Path to the file containing the data",
        required=True,
    )
    parser.add_argument(
        "-i",
        "--Iterations",
        type=int,
        help="How many iterations the algorithm should perform",
        required=True,
    )
    parser.add_argument(
        "-s", "--Size", type=int, help="Size of the tabu list", required=True
    )

    # 将参数传递给 main 函数
    main(parser.parse_args())
