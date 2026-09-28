# 高斯朴素贝叶斯示例

from matplotlib import pyplot as plt
from sklearn.datasets import load_iris
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB


def main() -> None:
    """
    使用 sklearn 函数实现的高斯朴素贝叶斯示例。
    使用 Iris 类型数据集演示该算法。
    """
    # 加载 Iris 数据集
    iris = load_iris()

    # 将数据集拆分为训练数据和测试数据
    x = iris["data"]  # 特征
    y = iris["target"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=1
    )

    # 高斯朴素贝叶斯
    nb_model = GaussianNB()
    nb_model.fit(x_train, y_train)
    y_pred = nb_model.predict(x_test)  # 对测试集进行预测

    # 显示混淆矩阵
    ConfusionMatrixDisplay.from_estimator(
        nb_model,
        x_test,
        y_test,
        display_labels=iris["target_names"],
        cmap="Blues",
        normalize="true",
    )
    plt.title("Normalized Confusion Matrix - IRIS Dataset")
    plt.show()

    final_accuracy = 100 * accuracy_score(y_true=y_test, y_pred=y_pred)
    print(f"The overall accuracy of the model is: {round(final_accuracy, 2)}%")


if __name__ == "__main__":
    main()
