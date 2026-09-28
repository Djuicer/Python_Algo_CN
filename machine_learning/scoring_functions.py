import numpy as np

""" Here I implemented the scoring functions.
    MAE, MSE, RMSE, RMSLE are included.

    Those are used for calculating differences between
    predicted values and actual values.

    Metrics are slightly differentiated. Sometimes squared, rooted,
    even log is used.

    Using log and roots can be perceived as tools for penalizing big
    errors. However, using appropriate metrics depends on the situations,
    and types of data
"""


# 平均绝对误差
def mae(predict, actual):
    """
    示例（为保证精度已四舍五入）：
    >>> actual = [1,2,3];predict = [1,4,3]
    >>> float(np.around(mae(predict,actual),decimals = 2))
    0.67

    >>> actual = [1,1,1];predict = [1,1,1]
    >>> float(mae(predict,actual))
    0.0
    """
    predict = np.array(predict)
    actual = np.array(actual)

    difference = abs(predict - actual)
    score = difference.mean()

    return score


# 均方误差
def mse(predict, actual):
    """
    示例（为保证精度已四舍五入）：
    >>> actual = [1,2,3];predict = [1,4,3]
    >>> float(np.around(mse(predict,actual),decimals = 2))
    1.33

    >>> actual = [1,1,1];predict = [1,1,1]
    >>> float(mse(predict,actual))
    0.0
    """
    predict = np.array(predict)
    actual = np.array(actual)

    difference = predict - actual
    square_diff = np.square(difference)

    score = square_diff.mean()
    return score


# Root 均方误差
def rmse(predict, actual):
    """
    示例（为保证精度已四舍五入）：
    >>> actual = [1,2,3];predict = [1,4,3]
    >>> float(np.around(rmse(predict,actual),decimals = 2))
    1.15

    >>> actual = [1,1,1];predict = [1,1,1]
    >>> float(rmse(predict,actual))
    0.0
    """
    predict = np.array(predict)
    actual = np.array(actual)

    difference = predict - actual
    square_diff = np.square(difference)
    mean_square_diff = square_diff.mean()
    score = np.sqrt(mean_square_diff)
    return score


# 均方根对数误差
def rmsle(predict, actual):
    """
    示例（为保证精度已四舍五入）：
    >>> float(np.around(rmsle(predict=[10, 2, 30], actual=[10, 10, 30]), decimals=2))
    0.75

    >>> float(rmsle(predict=[1, 1, 1], actual=[1, 1, 1]))
    0.0
    """
    predict = np.array(predict)
    actual = np.array(actual)

    log_predict = np.log(predict + 1)
    log_actual = np.log(actual + 1)

    difference = log_predict - log_actual
    square_diff = np.square(difference)
    mean_square_diff = square_diff.mean()

    score = np.sqrt(mean_square_diff)

    return score


# 平均偏差
def mbd(predict, actual):
    """
    This value is Negative, if the model underpredicts,
    positive, if it overpredicts.

    示例（为保证精度已四舍五入）：

    Here the model overpredicts
    >>> actual = [1,2,3];predict = [2,3,4]
    >>> float(np.around(mbd(predict,actual),decimals = 2))
    50.0

    Here the model underpredicts
    >>> actual = [1,2,3];predict = [0,1,1]
    >>> float(np.around(mbd(predict,actual),decimals = 2))
    -66.67
    """
    predict = np.array(predict)
    actual = np.array(actual)

    difference = predict - actual
    numerator = np.sum(difference) / len(predict)
    denumerator = np.sum(actual) / len(predict)
    # print(numerator, denumerator)
    score = float(numerator) / denumerator * 100

    return score


def manual_accuracy(predict, actual):
    return np.mean(np.array(actual) == np.array(predict))
