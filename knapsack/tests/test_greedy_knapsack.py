import unittest

import pytest

from knapsack import greedy_knapsack as kp


class TestClass(unittest.TestCase):
    """
    背包问题的测试用例。
    """

    def test_sorted(self) -> None:
        """
        kp.calc_profit 接收所需参数 (profit, weight, max_weight)，
        并检查返回答案是否与预期结果一致。
        """
        profit = [10, 20, 30, 40, 50, 60]
        weight = [2, 4, 6, 8, 10, 12]
        max_weight = 100
        assert kp.calc_profit(profit, weight, max_weight) == 210

    def test_negative_max_weight(self) -> None:
        """
        对任意负数 max_weight 值返回 ValueError。
        :return: ValueError
        """
        # profit = [10, 20, 30, 40, 50, 60]
        # weight = [2, 4, 6, 8, 10, 12]
        # max_weight = -15
        pytest.raises(ValueError, match=r"max_weight must greater than zero.")

    def test_negative_profit_value(self) -> None:
        """
        对列表中的任意负利润值返回 ValueError。
        :return: ValueError
        """
        # profit = [10, -20, 30, 40, 50, 60]
        # weight = [2, 4, 6, 8, 10, 12]
        # max_weight = 15
        pytest.raises(ValueError, match=r"Weight can not be negative.")

    def test_negative_weight_value(self) -> None:
        """
        对列表中的任意负重量值返回 ValueError。
        :return: ValueError
        """
        # profit = [10, 20, 30, 40, 50, 60]
        # weight = [2, -4, 6, -8, 10, 12]
        # max_weight = 15
        pytest.raises(ValueError, match=r"Profit can not be negative.")

    def test_null_max_weight(self) -> None:
        """
        对任意为零的 max_weight 值返回 ValueError。
        :return: ValueError
        """
        # profit = [10, 20, 30, 40, 50, 60]
        # weight = [2, 4, 6, 8, 10, 12]
        # max_weight = null
        pytest.raises(ValueError, match=r"max_weight must greater than zero.")

    def test_unequal_list_length(self) -> None:
        """
        当列表 profit 与 weight 的长度不相等时返回 IndexError。
        :return: IndexError
        """
        # profit = [10, 20, 30, 40, 50]
        # weight = [2, 4, 6, 8, 10, 12]
        # max_weight = 100
        pytest.raises(
            IndexError, match=r"The length of profit and weight must be same."
        )


if __name__ == "__main__":
    unittest.main()
