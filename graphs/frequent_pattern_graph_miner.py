"""
FP-GraphMiner - 网络图的快速频繁模式挖掘算法

一种新颖的频繁模式图挖掘算法 FP-GraphMiner
将一组网络图表示为频繁模式图（或FP图）。
该图可用于有效地挖掘频繁子图，包括最大
频繁子图和最大公共子图。

URL: https://www.researchgate.net/publication/235255851
"""

# fmt: off
edge_array = [
    ['ab-e1', 'ac-e3', 'ad-e5', 'bc-e4', 'bd-e2', 'be-e6', 'bh-e12', 'cd-e2', 'ce-e4',
     'de-e1', 'df-e8', 'dg-e5', 'dh-e10', 'ef-e3', 'eg-e2', 'fg-e6', 'gh-e6', 'hi-e3'],
    ['ab-e1', 'ac-e3', 'ad-e5', 'bc-e4', 'bd-e2', 'be-e6', 'cd-e2', 'de-e1', 'df-e8',
     'ef-e3', 'eg-e2', 'fg-e6'],
    ['ab-e1', 'ac-e3', 'bc-e4', 'bd-e2', 'de-e1', 'df-e8', 'dg-e5', 'ef-e3', 'eg-e2',
     'eh-e12', 'fg-e6', 'fh-e10', 'gh-e6'],
    ['ab-e1', 'ac-e3', 'bc-e4', 'bd-e2', 'bh-e12', 'cd-e2', 'df-e8', 'dh-e10'],
    ['ab-e1', 'ac-e3', 'ad-e5', 'bc-e4', 'bd-e2', 'cd-e2', 'ce-e4', 'de-e1', 'df-e8',
     'dg-e5', 'ef-e3', 'eg-e2', 'fg-e6']
]
# fmt: on


def get_distinct_edge(edge_array):
    """
    从多个图的边数组返回不同的边
    >>> sorted(get_distinct_edge(edge_array))
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    """
    distinct_edge = set()
    for row in edge_array:
        for item in row:
            distinct_edge.add(item[0])
    return list(distinct_edge)


def get_bitcode(edge_array, distinct_edge):
    """
    返回distinct_edge的位码
    """
    bitcode = ["0"] * len(edge_array)
    for i, row in enumerate(edge_array):
        for item in row:
            if distinct_edge in item[0]:
                bitcode[i] = "1"
                break
    return "".join(bitcode)


def get_frequency_table(edge_array):
    """
    返回频率表
    """
    distinct_edge = get_distinct_edge(edge_array)
    frequency_table = {}

    for item in distinct_edge:
        bit = get_bitcode(edge_array, item)
        # print('bit',bit)
        # bt=''.join(bit)
        s = bit.count("1")
        frequency_table[item] = [s, bit]
    # 按降序存储[独特边界，WT(Bitcode)，Bitcode]
    sorted_frequency_table = [
        [k, v[0], v[1]]
        for k, v in sorted(frequency_table.items(), key=lambda v: v[1][0], reverse=True)
    ]
    return sorted_frequency_table


def get_nodes(frequency_table):
    """
    返回节点
    格式节点={位码:表示位码的边}
    >>> get_nodes([['ab', 5, '11111'], ['ac', 5, '11111'], ['df', 5, '11111'],
    ...            ['bd', 5, '11111'], ['bc', 5, '11111']])
    {'11111': ['ab', 'ac', 'df', 'bd', 'bc']}
    """
    nodes = {}
    for _, item in enumerate(frequency_table):
        nodes.setdefault(item[2], []).append(item[0])
    return nodes


def get_cluster(nodes):
    """
    返回簇
    格式簇：{WT(bitcode):具有相同WT的节点}
    """
    cluster = {}
    for key, value in nodes.items():
        cluster.setdefault(key.count("1"), {})[key] = value
    return cluster


def get_support(cluster):
    """
    返回支持
    >>> get_support({5: {'11111': ['ab', 'ac', 'df', 'bd', 'bc']},
    ...              4: {'11101': ['ef', 'eg', 'de', 'fg'], '11011': ['cd']},
    ...              3: {'11001': ['ad'], '10101': ['dg']},
    ...              2: {'10010': ['dh', 'bh'], '11000': ['be'], '10100': ['gh'],
    ...                  '10001': ['ce']},
    ...              1: {'00100': ['fh', 'eh'], '10000': ['hi']}})
    [100.0, 80.0, 60.0, 40.0, 20.0]
    """
    return [i * 100 / len(cluster) for i in cluster]


def print_all() -> None:
    print("\nNodes\n")
    for key, value in nodes.items():
        print(key, value)
    print("\nSupport\n")
    print(support)
    print("\n Cluster \n")
    for key, value in sorted(cluster.items(), reverse=True):
        print(key, value)
    print("\n Graph\n")
    for key, value in graph.items():
        print(key, value)
    print("\n Edge List of Frequent subgraphs \n")
    for edge_list in freq_subgraph_edge_list:
        print(edge_list)


def create_edge(nodes, graph, cluster, c1) -> None:
    """
    在节点之间创建边
    """
    for i in cluster[c1]:
        count = 0
        c2 = c1 + 1
        while c2 < max(cluster.keys()):
            for j in cluster[c2]:
                """
                仅当条件满足时才创建边
                """
                if int(i, 2) & int(j, 2) == int(i, 2):
                    if tuple(nodes[i]) in graph:
                        graph[tuple(nodes[i])].append(nodes[j])
                    else:
                        graph[tuple(nodes[i])] = [nodes[j]]
                    count += 1
            if count == 0:
                c2 = c2 + 1
            else:
                break


def construct_graph(cluster, nodes):
    x = cluster[max(cluster.keys())]
    cluster[max(cluster.keys()) + 1] = "Header"
    graph = {}
    for i in x:
        if (["Header"],) in graph:
            graph[(["Header"],)].append(x[i])
        else:
            graph[(["Header"],)] = [x[i]]
    for i in x:
        graph[(x[i],)] = [["Header"]]
    i = 1
    while i < max(cluster) - 1:
        create_edge(nodes, graph, cluster, i)
        i = i + 1
    return graph


def my_dfs(graph, start, end, path=None) -> None:
    """
    找到从给定节点到 Header 节点的不同 DFS 遍历
    """
    path = (path or []) + [start]
    if start == end:
        paths.append(path)
    for node in graph[start]:
        if tuple(node) not in path:
            my_dfs(graph, tuple(node), end, path)


def find_freq_subgraph_given_support(s, cluster, graph) -> None:
    """
    查找多个频繁子图的边
    """
    k = int(s / 100 * (len(cluster) - 1))
    for i in cluster[k]:
        my_dfs(graph, tuple(cluster[k][i]), (["Header"],))


def freq_subgraphs_edge_list(paths):
    """
    返回频繁子图的边列表
    """
    freq_sub_el = []
    for edges in paths:
        el = []
        for j in range(len(edges) - 1):
            temp = list(edges[j])
            for e in temp:
                edge = (e[0], e[1])
                el.append(edge)
        freq_sub_el.append(el)
    return freq_sub_el


def preprocess(edge_array) -> None:
    """
    预处理边数组
    >>> preprocess([['ab-e1', 'ac-e3', 'ad-e5', 'bc-e4', 'bd-e2', 'be-e6', 'bh-e12',
    ...              'cd-e2', 'ce-e4', 'de-e1', 'df-e8', 'dg-e5', 'dh-e10', 'ef-e3',
    ...              'eg-e2', 'fg-e6', 'gh-e6', 'hi-e3']])

    """
    for i in range(len(edge_array)):
        for j in range(len(edge_array[i])):
            t = edge_array[i][j].split("-")
            edge_array[i][j] = t


if __name__ == "__main__":
    preprocess(edge_array)
    frequency_table = get_frequency_table(edge_array)
    nodes = get_nodes(frequency_table)
    cluster = get_cluster(nodes)
    support = get_support(cluster)
    graph = construct_graph(cluster, nodes)
    find_freq_subgraph_given_support(60, cluster, graph)
    paths: list = []
    freq_subgraph_edge_list = freq_subgraphs_edge_list(paths)
    print_all()
