"""
检查给定图中是否存在循环的程序
"""


def check_cycle(graph: dict) -> bool:
    """
    如果图是循环的，则返回True，否则返回False
    >>> check_cycle(graph={0:[], 1:[0, 3], 2:[0, 4], 3:[5], 4:[5], 5:[]})
    False
    >>> check_cycle(graph={0:[1, 2], 1:[2], 2:[0, 3], 3:[3]})
    True
    """
    # 跟踪访问过的节点
    visited: set[int] = set()
    # 要检测后边，请跟踪递归堆栈中当前的顶点
    rec_stk: set[int] = set()
    return any(
        node not in visited and depth_first_search(graph, node, visited, rec_stk)
        for node in graph
    )


def depth_first_search(graph: dict, vertex: int, visited: set, rec_stk: set) -> bool:
    """
    对所有邻居重复发生。
    如果访问了任何邻居并且在 rec_stk 中，则图是循环的。
    >>> graph = {0:[], 1:[0, 3], 2:[0, 4], 3:[5], 4:[5], 5:[]}
    >>> vertex, visited, rec_stk = 0, set(), set()
    >>> depth_first_search(graph, vertex, visited, rec_stk)
    False
    """
    # 将当前节点标记为已访问并添加到递归堆栈
    visited.add(vertex)
    rec_stk.add(vertex)

    for node in graph[vertex]:
        if node not in visited:
            if depth_first_search(graph, node, visited, rec_stk):
                return True
        elif node in rec_stk:
            return True

    # 在函数结束之前需要从递归堆栈中删除该节点
    rec_stk.remove(vertex)
    return False


if __name__ == "__main__":
    from doctest import testmod

    testmod()
