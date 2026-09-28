#  Created by: Ramy-Badr-Ahmed (https://github.com/Ramy-Badr-Ahmed)
#  在 Pull Request: #11532
#  https://github.com/TheAlgorithms/Python/pull/11532
#
#  Please mention me (@Ramy-Badr-Ahmed) 在 任意 问题 或 pull request
#  寻址 bugs/corrections 到 此 文件。
#  Thank you!

from __future__ import annotations


class KDNode:
    """
    表示 一个节点 在 KD-树。

    属性：
        点: 点 存储 在 此 节点。
        左: 左 子节点。
        右: 右子节点 节点。
    """

    def __init__(
        self,
        point: list[float],
        left: KDNode | None = None,
        right: KDNode | None = None,
    ) -> None:
        """
        Initializes KDNode 带有 给定 点 并且 子节点 节点。

        参数：
            点 (列表[浮点数]): 点 存储 在 此 节点。
            左 (可选[KDNode]): 左 子节点。
            右 (可选[KDNode]): 右子节点 节点。
        """
        self.point = point
        self.left = left
        self.right = right
