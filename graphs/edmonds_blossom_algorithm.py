from collections import deque


class BlossomAuxData:
    """在花算法执行期间保存辅助数据的类。"""

    def __init__(
        self,
        queue: deque,
        parent: list[int],
        base: list[int],
        in_blossom: list[bool],
        match: list[int],
        in_queue: list[bool],
    ) -> None:
        """
        初始化 BlossomAuxData 实例。

        参数：
            队列：用于BFS处理的双端队列。
            父节点：增广路径中的父节点列表。
            base：每个顶点的基顶点列表。
            in_blossom：布尔列表，指示顶点是否花状态。
            match：匹配顶点的列表。
            in_queue：布尔列表，指示顶点是否在队列中。
        """
        self.queue = queue
        self.parent = parent
        self.base = base
        self.in_blossom = in_blossom
        self.match = match
        self.in_queue = in_queue


class BlossomData:
    """用于封装与图中花朵相关的数据的类。"""

    def __init__(
        self,
        aux_data: BlossomAuxData,
        vertex_u: int,
        vertex_v: int,
        lowest_common_ancestor: int,
    ) -> None:
        """
        初始化 BlossomData 实例。

        参数：
            aux_data：与花相关的辅助数据。
            vertex_u： 葡萄在一个顶点。
            vertex_v：花中的另一个顶点。
            lowest_common_ancestor：vertex_u和vertex_v的最低共同祖先。
        """
        self.aux_data = aux_data
        self.vertex_u = vertex_u
        self.vertex_v = vertex_v
        self.lowest_common_ancestor = lowest_common_ancestor


class EdmondsBlossomAlgorithm:
    UNMATCHED = -1  # 表示不匹配顶点的常量

    @staticmethod
    def maximum_matching(edges: list[list[int]], vertex_count: int) -> list[list[int]]:
        """
        使用 Edmonds Blossom 算法找到最佳匹配。

        参数：
            边：表示为顶点对的边列表。
            vertex_count：顶点的顶点。

        返回：
            列表列表形式的匹配对的列表。
        """
        # 为图创建邻接表
        graph: list[list[int]] = [[] for _ in range(vertex_count)]

        # 用边填充图
        for edge in edges:
            u, v = edge
            graph[u].append(v)
            graph[v].append(u)

        # 所有顶点最初都是不匹配的
        match: list[int] = [EdmondsBlossomAlgorithm.UNMATCHED] * vertex_count
        parent: list[int] = [EdmondsBlossomAlgorithm.UNMATCHED] * vertex_count
        # 每个顶点最初都是它自己的基础
        base: list[int] = list(range(vertex_count))
        in_blossom: list[bool] = [False] * vertex_count
        # 跟踪 BFS 队列中的边
        in_queue: list[bool] = [False] * vertex_count

        # 寻找最大匹配的主要逻辑
        for u in range(vertex_count):
            # 只考虑不匹配的顶点
            if match[u] == EdmondsBlossomAlgorithm.UNMATCHED:
                # 广度优先搜索初始化
                parent = [EdmondsBlossomAlgorithm.UNMATCHED] * vertex_count
                base = list(range(vertex_count))
                in_blossom = [False] * vertex_count
                in_queue = [False] * vertex_count

                queue = deque([u])  # 从不匹配的顶点开始BFS
                in_queue[u] = True

                augmenting_path_found = False

                # BFS寻找增广路径
                while queue and not augmenting_path_found:
                    current = queue.popleft()  # 获取当前顶点
                    for y in graph[current]:  # 探索相邻顶点
                        # 如果我们正在查看当前比赛，则跳过
                        if match[current] == y:
                            continue

                        if base[current] == base[y]:  # 避免自循环
                            continue

                        if parent[y] == EdmondsBlossomAlgorithm.UNMATCHED:
                            # 情况1：y不匹配；
                            # 我们找到了一条增广路径
                            if match[y] == EdmondsBlossomAlgorithm.UNMATCHED:
                                parent[y] = current  # 更新父级
                                augmenting_path_found = True
                                # 沿着这条路增强
                                EdmondsBlossomAlgorithm.update_matching(
                                    match, parent, y
                                )
                                break

                            # 情况2：y匹配；
                            # 将 y 的匹配添加到队列中
                            z = match[y]
                            parent[y] = current
                            parent[z] = y
                            if not in_queue[z]:  # 如果 z 尚未在队列中
                                queue.append(z)
                                in_queue[z] = True
                        else:
                            # 情况3：现在有父节点；
                            # 检查周期/花
                            base_u = EdmondsBlossomAlgorithm.find_base(
                                base, parent, current, y
                            )
                            if base_u != EdmondsBlossomAlgorithm.UNMATCHED:
                                EdmondsBlossomAlgorithm.contract_blossom(
                                    BlossomData(
                                        BlossomAuxData(
                                            queue,
                                            parent,
                                            base,
                                            in_blossom,
                                            match,
                                            in_queue,
                                        ),
                                        current,
                                        y,
                                        base_u,
                                    )
                                )

        # 创建匹配对的结果列表
        matching_result: list[list[int]] = []
        for v in range(vertex_count):
            if (
                match[v] != EdmondsBlossomAlgorithm.UNMATCHED and v < match[v]
            ):  # 确保对是唯一的
                matching_result.append([v, match[v]])

        return matching_result

    @staticmethod
    def update_matching(
        match: list[int], parent: list[int], matched_vertex: int
    ) -> None:
        """
        根据找到的增广路径更新匹配。

        参数：
            match：当前的匹配列表。
            Parent：BFS遍历的父列表。
            matched_vertex：增广路径结束的顶点。
        """
        while matched_vertex != EdmondsBlossomAlgorithm.UNMATCHED:
            v = parent[matched_vertex]  # 获取父顶点
            next_match = match[v]  # 存储下一场比赛
            match[v] = matched_vertex  # 更新 v 的匹配
            match[matched_vertex] = v  # 更新 matched_vertex 的匹配
            matched_vertex = next_match  # 移动到下一个顶点

    @staticmethod
    def find_base(
        base: list[int], parent: list[int], vertex_u: int, vertex_v: int
    ) -> int:
        """
        找到花朵的基部。

        参数：
            base：每个顶点的基础数据库。
            Parent：来自BFS的父备份。
            vertex_u：花的一个终点。
            vertex_v：花的另一个端点。

        返回：
            vertex_u和vertex_v的最低共同祖先在花。
        """
        visited: list[bool] = [False] * len(base)

        # 标记vertex_u的祖先
        current_vertex_u = vertex_u
        while True:
            current_vertex_u = base[current_vertex_u]
            # 将此基地标记为已访问
            visited[current_vertex_u] = True
            if parent[current_vertex_u] == EdmondsBlossomAlgorithm.UNMATCHED:
                break
            current_vertex_u = parent[current_vertex_u]

        # 找到vertex_v的共同祖先
        current_vertex_v = vertex_v
        while True:
            current_vertex_v = base[current_vertex_v]
            # 检查我们是否已经访问过这个基地
            if visited[current_vertex_v]:
                return current_vertex_v
            current_vertex_v = parent[current_vertex_v]

    @staticmethod
    def contract_blossom(blossom_data: BlossomData) -> None:
        """
        契约匹配过程中发现的花朵。

        参数：
            blossom_data：与要承包商的相关数据。
        """
        # 标记花中的顶点
        for x in range(
            blossom_data.vertex_u,
            blossom_data.aux_data.base[blossom_data.vertex_u]
            != blossom_data.lowest_common_ancestor,
        ):
            base_x = blossom_data.aux_data.base[x]
            match_base_x = blossom_data.aux_data.base[blossom_data.aux_data.match[x]]
            # 将底座标记为盛开的花朵
            blossom_data.aux_data.in_blossom[base_x] = True
            blossom_data.aux_data.in_blossom[match_base_x] = True

        for x in range(
            blossom_data.vertex_v,
            blossom_data.aux_data.base[blossom_data.vertex_v]
            != blossom_data.lowest_common_ancestor,
        ):
            base_x = blossom_data.aux_data.base[x]
            match_base_x = blossom_data.aux_data.base[blossom_data.aux_data.match[x]]
            # 将底座标记为盛开的花朵
            blossom_data.aux_data.in_blossom[base_x] = True
            blossom_data.aux_data.in_blossom[match_base_x] = True

        # 更新所有标记顶点的基础
        for i in range(len(blossom_data.aux_data.base)):
            if blossom_data.aux_data.in_blossom[blossom_data.aux_data.base[i]]:
                # 与最低共同祖先的契约
                blossom_data.aux_data.base[i] = blossom_data.lowest_common_ancestor
                if not blossom_data.aux_data.in_queue[i]:
                    # 添加到队列（如果尚不存在）
                    blossom_data.aux_data.queue.append(i)
                    blossom_data.aux_data.in_queue[i] = True
