"""
k 近邻（k-Nearest Neighbors, kNN）是一种用于分类的简单非参数监督学习算法。
给定带标签的训练数据后，算法根据某种距离度量，使用给定点的 k 个最近邻对其
分类。邻居中出现次数最多的标签成为该点的标签，即通过多数表决决定标签。

本实现采用常用的欧几里得距离度量，也可以使用其他距离度量。

Reference: https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm
"""

from collections import Counter
from heapq import nsmallest

import numpy as np
from numpy.typing import NDArray
from sklearn import datasets
from sklearn.model_selection import train_test_split


class KNN:
    def __init__(
        self,
        train_data: NDArray[np.float64],
        train_target: NDArray[np.int64],
        class_labels: list[str],
    ) -> None:
        """
        使用给定训练数据和类别标签创建 kNN 分类器
        """
        self.data = zip(train_data, train_target)
        self.labels = class_labels

    @staticmethod
    def _euclidean_distance(a: NDArray[np.float64], b: NDArray[np.float64]) -> float:
        """
        计算两点之间的欧几里得距离
        >>> KNN._euclidean_distance(np.array([0, 0]), np.array([3, 4]))
        5.0
        >>> KNN._euclidean_distance(np.array([1, 2, 3]), np.array([1, 8, 11]))
        10.0
        """
        return float(np.linalg.norm(a - b))

    def classify(self, pred_point: NDArray[np.float64], k: int = 5) -> str:
        """
        使用 kNN 算法对给定点进行分类
        >>> train_X = np.array(
        ...     [[0, 0], [1, 0], [0, 1], [0.5, 0.5], [3, 3], [2, 3], [3, 2]]
        ... )
        >>> train_y = np.array([0, 0, 0, 0, 1, 1, 1])
        >>> classes = ['A', 'B']
        >>> knn = KNN(train_X, train_y, classes)
        >>> point = np.array([1.2, 1.2])
        >>> knn.classify(point)
        'A'
        """
        # 所有点与待分类点之间的距离
        distances = (
            (self._euclidean_distance(data_point[0], pred_point), data_point[1])
            for data_point in self.data
        )

        # 选择距离最短的 k 个点
        votes = (i[1] for i in nsmallest(k, distances))

        # 将该点归入出现次数最多的类别
        result = Counter(votes).most_common(1)[0][0]
        return self.labels[result]


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    iris = datasets.load_iris()

    X = np.array(iris["data"])
    y = np.array(iris["target"])
    iris_classes = iris["target_names"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    iris_point = np.array([4.4, 3.1, 1.3, 1.4])
    classifier = KNN(X_train, y_train, iris_classes)
    print(classifier.classify(iris_point, k=3))
