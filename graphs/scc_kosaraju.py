from __future__ import annotations


def dfs(u) -> None:
    global graph, reversed_graph, scc, component, visit, stack
    if visit[u]:
        return
    visit[u] = True
    for v in graph[u]:
        dfs(v)
    stack.append(u)


def dfs2(u) -> None:
    global graph, reversed_graph, scc, component, visit, stack
    if visit[u]:
        return
    visit[u] = True
    component.append(u)
    for v in reversed_graph[u]:
        dfs2(v)


def kosaraju():
    global graph, reversed_graph, scc, component, visit, stack
    for i in range(n):
        dfs(i)
    visit = [False] * n
    for i in stack[::-1]:
        if visit[i]:
            continue
        component = []
        dfs2(i)
        scc.append(component)
    return scc


if __name__ == "__main__":
    # n - 节点数，m - 边数
    n, m = list(map(int, input().strip().split()))

    graph: list[list[int]] = [[] for _ in range(n)]  # 图
    reversed_graph: list[list[int]] = [[] for i in range(n)]  # 反转图
    # 输入图数据（边）
    for _ in range(m):
        u, v = list(map(int, input().strip().split()))
        graph[u].append(v)
        reversed_graph[v].append(u)

    stack: list[int] = []
    visit: list[bool] = [False] * n
    scc: list[int] = []
    component: list[int] = []
    print(kosaraju())
