# 随机森林分类器示例

from matplotlib import pyplot as plt
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split


def main() -> None:
    """
    随机森林分类器示例 using sklearn function.
    Iris type dataset is used to demonstrate algorithm.
    """
    # 加载 Iris 数据集
    iris = load_iris()

    # 将数据集拆分为训练数据和测试数据
    x = iris["data"]  # 特征
    y = iris["target"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=1
    )

    # 随机森林分类器
    rand_for = RandomForestClassifier(random_state=42, n_estimators=100)
    rand_for.fit(x_train, y_train)

    # 显示分类器的混淆矩阵
    ConfusionMatrixDisplay.from_estimator(
        rand_for,
        x_test,
        y_test,
        display_labels=iris["target_names"],
        cmap="Blues",
        normalize="true",
    )
    plt.title("Normalized Confusion Matrix - IRIS Dataset")
    plt.show()


if __name__ == "__main__":
    main()
